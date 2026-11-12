"""Контрольные случаи без настоящих профилей и внешних сетевых запросов."""

import asyncio
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.api.genes import router
from src.api.genes.dependencies import get_profile_storage
from src.api.patients.patients import router as patients_router
from src.database import Base
from src.db_depends import get_async_db
from src.models.patients import Patient
from src.schemas.gene_analysis import GeneAnalysisReport
from src.services.gene_analysis.annotations import AnnotationError, _valid_annotation_batch
from src.services.gene_analysis.clinvar import extract_clinvar_significance
from src.services.gene_analysis.config import PROJECT_ROOT
from src.services.gene_analysis.errors import GeneAnalysisError
from src.services.gene_analysis.genotype_rules import evaluate_complex_genotypes
from src.services.gene_analysis.pgs_interpretation import interpret_pgs
from src.services.gene_analysis.pgs_scoring import _pgs_alleles_match, calculate_pgs, compute_pgs_scores
from src.services.gene_analysis.profile_storage import ProfileStorage, atomic_json
from src.services.gene_analysis.service import analyze_profile
from src.services.gene_analysis.vcf_parser import parse_vcf
from gene_analysis_fixtures import example_report


def vcf_text(rows: str = "1\t100\trs1\tA\tG\t.\tPASS\t.\tGT\t0/1\n", reference: str = "") -> bytes:
    return ("##fileformat=VCFv4.2\n" + reference +
            '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n' +
            '##FORMAT=<ID=PS,Number=1,Type=Integer,Description="Phase set">\n' +
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYNTHETIC\n" + rows).encode()


def weights(count: int = 1) -> pd.DataFrame:
    return pd.DataFrame([{"hm_rsID": f"rs{index + 1}", "hm_chr": "1", "hm_pos": 100 + index,
                          "effect_allele": "G", "other_allele": "A", "effect_weight": 0.5,
                          "allelefrequency_effect": 0.2} for index in range(count)])


class StorageCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.storage = ProfileStorage(self.root / "data")

    def upload(self, content: bytes | None = None, patient_id: int = 1):
        with self.storage.lock(patient_id):
            return self.storage.replace(patient_id, "test.vcf", io.BytesIO(content or vcf_text()))

    def parse(self, content: bytes):
        path = self.root / "input.vcf"
        path.write_bytes(content)
        return parse_vcf(path)

    def test_parser_preserves_reference_and_skips_invalid_calls(self):
        parsed = self.parse(vcf_text("".join(f"1\t100\trs1\tA\tG\t.\tPASS\t.\tGT\t{gt}\n"
                                             for gt in ("0/0", "0/1", "1/1", "./.", "0/.", "2/2"))))
        self.assertEqual(len(parsed.variants), 3)
        self.assertEqual(parsed.skipped_records, 3)
        self.assertEqual(parsed.build_source, "assumed")

    def test_rejects_build_multiple_samples_and_empty(self):
        invalid = [vcf_text(reference="##reference=GRCh38\n"), b"", b"not vcf", b"##fileformat=VCFv4.2\n",
                   vcf_text(reference="##assembly=GRCh38\n"),
                   vcf_text().replace(b"SYNTHETIC\n", b"SYNTHETIC\tSECOND\n"), vcf_text(rows="")]
        for data in invalid:
            with self.subTest(data=data[:30]), self.assertRaises(GeneAnalysisError):
                self.parse(data)
        self.assertEqual(self.parse(vcf_text(reference="##reference=GRCh37\n")).build_source, "declared")

    def test_replacement_isolation_failure_and_size(self):
        old = self.upload()
        other = self.upload(patient_id=2)
        (self.storage.profile_dir(1, old) / "analysis.json").write_text("old")
        with self.assertRaises(GeneAnalysisError):
            self.storage.replace(1, "invalid.vcf", io.BytesIO(b"invalid"))
        self.assertEqual(self.storage.current(1), old)
        self.storage.max_bytes = 5
        with self.assertRaises(GeneAnalysisError) as error:
            self.upload()
        self.assertEqual(error.exception.status_code, 413)
        self.storage.max_bytes = 100000
        new = self.storage.replace(1, "../../safe.vcf", io.BytesIO(vcf_text()))
        self.assertEqual(new.filename, "safe.vcf")
        self.assertFalse(self.storage.profile_dir(1, old).exists())
        self.assertEqual(self.storage.current(2), other)
        self.assertEqual(len(list(self.storage.patient_dir(1).iterdir())), 2)

    def test_lock_conflict_and_release(self):
        with self.storage.lock(1):
            with self.assertRaises(GeneAnalysisError) as error:
                with ProfileStorage(self.storage.root).lock(1):
                    pass
            self.assertEqual(error.exception.status_code, 409)
        with self.storage.lock(1):
            pass

    def test_atomic_write_keeps_previous_file(self):
        path = self.root / "report.json"
        atomic_json(path, {"old": True})
        with patch.object(Path, "replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                atomic_json(path, {"new": True})
        self.assertEqual(json.loads(path.read_text()), {"old": True})
        self.assertFalse(list(self.root.glob("*.tmp")))

    @patch("src.services.gene_analysis.service.download_pgs_scoring_file", return_value=None)
    @patch("src.services.gene_analysis.service.annotate_variants", side_effect=AnnotationError("offline"))
    def test_partial_report_is_saved_and_never_recalculated(self, annotation, scoring):
        profile = self.upload()
        first = analyze_profile(1, self.storage)
        second = analyze_profile(1, self.storage)
        self.assertEqual(first, second)
        self.assertEqual(annotation.call_count, 1)
        self.assertEqual(first.status, "partial")
        self.assertEqual(first.clinvar.status, "unavailable")
        self.assertIsNone(first.summary.other_candidate_variants_count)
        self.assertEqual(len(first.polygenic_scores.items), 14)
        self.assertEqual(len(first.genotype_rules.items), 7)
        self.assertNotIn("NaN", first.model_dump_json())
        path = self.storage.profile_dir(1, profile) / "analysis.json"
        path.write_text("broken")
        with self.assertRaises(GeneAnalysisError) as error:
            analyze_profile(1, self.storage)
        self.assertEqual(error.exception.status_code, 409)
        self.upload()
        analyze_profile(1, self.storage)
        self.assertEqual(annotation.call_count, 2)

    @patch("src.services.gene_analysis.service.download_pgs_scoring_file", return_value=None)
    @patch("src.services.gene_analysis.service.annotate_variants", return_value=[])
    def test_failed_report_write_does_not_cache_success(self, annotation, scoring):
        profile = self.upload()
        with patch.object(self.storage, "save_report", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                analyze_profile(1, self.storage)
        self.assertFalse((self.storage.profile_dir(1, profile) / "analysis.json").exists())
        analyze_profile(1, self.storage)
        self.assertEqual(annotation.call_count, 2)

    def test_annotation_completeness(self):
        self.assertTrue(_valid_annotation_batch([{"query": "rs1", "notfound": True}], ["rs1"]))
        self.assertFalse(_valid_annotation_batch([], ["rs1"]))

    def test_rules_ambiguous_and_phase(self):
        rows = "19\t1\trs429358\tT\tC\t.\tPASS\t.\tGT:PS\t0|1:10\n19\t2\trs7412\tC\tT\t.\tPASS\t.\tGT:PS\t0|1:10\n"
        results = evaluate_complex_genotypes(self.parse(vcf_text(rows)).variants)
        self.assertEqual(results[0]["reason_code"], "unsupported_diplotype")
        # cis and trans produce different diplotypes; neither may be guessed without phase.
        for modified in (rows.replace("0|1:10", "0/1:10"), rows.replace("0|1:10\n19", "0|1:11\n19")):
            self.assertEqual(evaluate_complex_genotypes(self.parse(vcf_text(modified)).variants)[0]["reason_code"], "unknown_phase")
        duplicate = rows + rows.splitlines()[0] + "\n"
        self.assertEqual(evaluate_complex_genotypes(self.parse(vcf_text(duplicate)).variants)[0]["reason_code"], "ambiguous_variant")
        trans = rows.replace("rs7412\tC\tT\t.\tPASS\t.\tGT:PS\t0|1", "rs7412\tC\tT\t.\tPASS\t.\tGT:PS\t1|0")
        self.assertEqual(evaluate_complex_genotypes(self.parse(vcf_text(trans)).variants)[0]["genotype"], "e2/e4")

    def test_clinvar_exact_match_and_dedup(self):
        parsed = self.parse(vcf_text())
        annotation = {"query": "rs1", "_id": "chr1:g.100A>G", "clinvar": {
            "chrom": "1", "ref": "A", "alt": "G", "hg19": {"start": 100, "end": 100},
            "gene": {"symbol": "GENE"}, "rcv": [
                {"accession": "RCV1", "clinical_significance": "pathogenic", "conditions": {"name": "A"}},
                {"accession": "RCV2", "clinical_significance": "uncertain significance", "conditions": {"name": "B"}},
            ]}}
        frame = extract_clinvar_significance([annotation, annotation], parsed.variants)
        self.assertEqual(len(frame), 2)
        annotation["clinvar"]["alt"] = "T"
        self.assertTrue(extract_clinvar_significance([annotation], parsed.variants).empty)

    def test_pgs_dosage_imputation_mismatch_and_legacy_parity(self):
        parsed = self.parse(vcf_text()).variants
        result = calculate_pgs(parsed, weights(2))
        self.assertEqual((result["matched"], result["imputed"], result["skipped"]), (1, 1, 0))
        self.assertAlmostEqual(result["score"], 0.7)
        mismatch = parsed.copy()
        mismatch["pos"] = 200
        result = calculate_pgs(mismatch, weights(2))
        self.assertEqual((result["matched"], result["imputed"], result["skipped"]), (0, 1, 1))
        spec = importlib.util.spec_from_file_location("legacy_analysis", PROJECT_ROOT / "scripts/genes_analysis/analysis.py")
        legacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(legacy)
        self.assertEqual(calculate_pgs(parsed, weights(2)), legacy.calculate_pgs(parsed, weights(2)))
        for gt, expected in (("0/0", 0), ("0/1", 0.5), ("1/1", 1)):
            frame = self.parse(vcf_text().replace(b"0/1", gt.encode())).variants
            self.assertEqual(calculate_pgs(frame, weights())["score"], expected)

    def test_pgs_coverage_threshold(self):
        model = {"pgs_id": "synthetic", "trait": "test", "variants_count": 10}
        for count, expected in ((2, "not_evaluated"), (3, "research_score")):
            rows = "".join(f"1\t{100+i}\trs{i+1}\tA\tG\t.\tPASS\t.\tGT\t0/1\n" for i in range(count))
            result = compute_pgs_scores(self.parse(vcf_text(rows)).variants, [model], lambda _: weights(10))[0]
            self.assertEqual(result["status"], expected)

    def test_reference_absent_and_zero_variance(self):
        frame = self.parse(vcf_text()).variants
        scores = [{"pgs_id": "PGS000010", "status": "research_score"}]
        interpret_pgs(frame, scores, lambda _: weights(), _pgs_alleles_match, self.root / "missing.npz")
        self.assertEqual(scores[0]["eur_reason_code"], "reference_unavailable")
        path = self.root / "reference.npz"
        np.savez(path, rsids=np.array(["rs1"]), samples=np.array(["a", "b", "c"]),
                 chrom=np.array(["1"]), pos=np.array([100]), alleles=np.array([[[b"A", b"A"]]*3]))
        interpret_pgs(frame, scores, lambda _: weights(), _pgs_alleles_match, path)
        self.assertEqual(scores[0]["eur_reason_code"], "insufficient_reference_overlap")

    def test_reference_hr_gate_and_legacy_parity(self):
        path = self.root / "reference.npz"
        np.savez(path, rsids=np.array([f"rs{i+1}" for i in range(10)]),
                 samples=np.array(["a", "b", "c"]), chrom=np.array(["1"]*10),
                 pos=np.arange(100, 110),
                 alleles=np.array([[[b"A", b"A"], [b"A", b"G"], [b"G", b"G"]]]*10))
        for count, has_hr in ((3, False), (7, True), (10, True)):
            rows = "".join(f"1\t{100+i}\trs{i+1}\tA\tG\t.\tPASS\t.\tGT\t0/1\n" for i in range(count))
            frame = self.parse(vcf_text(rows)).variants
            scores = [{"pgs_id": "PGS000010", "status": "research_score"}]
            interpret_pgs(frame, scores, lambda _: weights(10), _pgs_alleles_match, path)
            self.assertEqual(scores[0]["eur_percentile"], 50.)
            self.assertEqual("eur_relative_hr" in scores[0], has_hr)
            spec = importlib.util.spec_from_file_location("legacy_pgs", PROJECT_ROOT / "scripts/genes_analysis/pgs_interpretation.py")
            legacy = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(legacy)
            original = [{"pgs_id": "PGS000010", "status": "research_score"}]
            legacy.interpret_pgs(frame, original, lambda _: weights(10), _pgs_alleles_match, path)
            for key in ("eur_percentile", "eur_r2", "eur_z", "eur_percentile_interval", "eur_relative_hr"):
                self.assertEqual(scores[0].get(key), original[0].get(key))

    def test_full_contract_and_evidence_links(self):
        report = example_report()
        self.assertEqual(report.status, "complete")
        self.assertEqual(len(report.summary.findings), 1)
        self.assertEqual(report.summary.findings[0].genes, ["DHCR7"])
        self.assertEqual(len(report.summary.polygenic_overview), 7)
        data = report.model_dump(mode="json")
        self.assertEqual(GeneAnalysisReport.model_validate(data), report)
        data["summary"]["findings"][0]["evidence_refs"][0]["item_id"] = "missing"
        with self.assertRaises(ValueError):
            GeneAnalysisReport.model_validate(data)
        data = report.model_dump(mode="json")
        data["polygenic_scores"]["items"][0]["raw_score"] = float("nan")
        with self.assertRaises(ValueError):
            GeneAnalysisReport.model_validate(data)

    def test_cache_import_idempotent(self):
        from src.services.gene_analysis.cache_import import import_caches
        source = self.root / "legacy"
        (source / ".myvariant_cache").mkdir(parents=True)
        (source / ".myvariant_cache" / "batch.json").write_text('[{"query":"rs1","notfound":true}]')
        (source / ".myvariant_cache" / "broken.json").write_text('broken')
        self.assertEqual(import_caches(source, self.storage.root), 1)
        self.assertEqual(import_caches(source, self.storage.root), 0)
        self.assertTrue((source / ".myvariant_cache" / "batch.json").exists())


class ApiCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.storage = ProfileStorage(self.root / "data")
        self.engine = create_async_engine(f"sqlite+aiosqlite:///{self.root / 'test.db'}")
        self.sessions = async_sessionmaker(self.engine, expire_on_commit=False)

        async def initialize():
            async with self.engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            async with self.sessions() as session:
                session.add_all([Patient(id=1, name="Тест", surname="Один", age=40),
                                 Patient(id=2, name="Тест", surname="Два", age=30)])
                await session.commit()
        asyncio.run(initialize())

        async def database():
            async with self.sessions() as session:
                yield session
        app = FastAPI()
        app.include_router(router, prefix="/api/patients/{patient_id}")
        app.include_router(patients_router, prefix="/api")
        app.dependency_overrides[get_async_db] = database
        app.dependency_overrides[get_profile_storage] = lambda: self.storage
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        asyncio.run(self.engine.dispose())
        self.temp.cleanup()

    @patch("src.services.gene_analysis.service.download_pgs_scoring_file", return_value=None)
    @patch("src.services.gene_analysis.service.annotate_variants", return_value=[])
    def test_http_lifecycle(self, annotation, scoring):
        base = "/api/patients/1/genes"
        self.assertEqual(self.client.get(base + "/profile").json(), {"profile": None})
        self.assertEqual(self.client.get(base + "/analysis").status_code, 404)
        self.assertEqual(self.client.get("/api/patients/99/genes/profile").status_code, 404)
        response = self.client.post(base + "/profile", files={"file": ("test.vcf", vcf_text())})
        self.assertEqual(response.status_code, 200, response.text)
        old_id = response.json()["profile"]["id"]
        first = self.client.get(base + "/analysis")
        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(first.json(), self.client.get(base + "/analysis").json())
        self.assertEqual(annotation.call_count, 1)
        self.assertEqual(self.client.post(base + "/profile", files={"file": ("invalid.vcf", b"bad")}).status_code, 422)
        self.assertEqual(self.client.get(base + "/profile").json()["profile"]["id"], old_id)
        replacement = self.client.post(base + "/profile", files={"file": ("new.vcf", vcf_text())})
        self.assertEqual(replacement.status_code, 200)
        self.assertNotEqual(replacement.json()["profile"]["id"], old_id)
        updated = self.client.get(base + "/analysis")
        self.assertEqual(updated.status_code, 200, updated.text)
        self.assertEqual(annotation.call_count, 2)
        self.assertEqual(self.client.get("/api/patients/2/genes/profile").json(), {"profile": None})
        with self.storage.lock(1):
            self.assertEqual(self.client.get(base + "/analysis").status_code, 409)
            self.assertEqual(self.client.delete("/api/patients/1").status_code, 409)
        self.assertEqual(self.client.delete("/api/patients/1").status_code, 204)
        self.assertFalse(self.storage.patient_dir(1).exists())

    def test_main_openapi_examples(self):
        from src.main import app
        with TestClient(app) as client:
            schema = client.get("/openapi.json")
            self.assertEqual(schema.status_code, 200)
            examples = schema.json()["paths"]["/api/patients/{patient_id}/genes/analysis"]["get"]["responses"]["200"]["content"]["application/json"]["examples"]
            for name in ("complete", "partial"):
                report = GeneAnalysisReport.model_validate(examples[name]["value"])
                self.assertEqual(report.status, name)
            self.assertEqual(client.get("/docs").status_code, 200)

    def test_local_frontend_cors(self):
        from src.main import app

        with TestClient(app) as client:
            for origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
                with self.subTest(origin=origin):
                    response = client.options(
                        "/api/patients/1/genes/profile",
                        headers={
                            "Origin": origin,
                            "Access-Control-Request-Method": "POST",
                            "Access-Control-Request-Headers": "content-type",
                        },
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response.headers["access-control-allow-origin"], origin
                    )
                    self.assertIn(
                        "POST", response.headers["access-control-allow-methods"]
                    )


if __name__ == "__main__":
    unittest.main()
