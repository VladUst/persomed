import Link from "@mui/material/Link";
import type { ClinvarItem } from "../../model/report";
import {
  clinvarEvaluationDate,
  clinvarReviewStatus,
  clinvarSignificance,
  clinvarZygosity,
} from "../clinvarFormatting";
import { Field } from "./DetailFields";

export const ClinvarDetail = ({ item }: { item: ClinvarItem }) => (
  <>
    <Field label="Гены" value={item.genes.join(", ")} />
    <Field
      label={
        item.category === "drug_response"
          ? "Ответ на препарат"
          : "Заболевание или признак"
      }
      value={item.conditions.join("; ")}
    />
    <Field
      label="Вариант"
      value={`${item.variant.genome_build} · chr${item.variant.chromosome}:${item.variant.position} ${item.variant.ref}>${item.variant.alt}`}
    />
    <Field label="rsID" value={item.variant.rsid} />
    <Field
      label="Генотип"
      value={`${item.genotype} · ${clinvarZygosity(item.zygosity)}`}
    />
    <Field
      label="Заключение источника"
      value={clinvarSignificance(item.significance.original)}
    />
    <Field label="Номер записи ClinVar" value={item.accession} />
    <Field
      label="Статус проверки"
      value={clinvarReviewStatus(item.review_status)}
    />
    <Field
      label="Дата оценки"
      value={clinvarEvaluationDate(item.last_evaluated)}
    />
    {item.source_url && (
      <Field
        label="Источник"
        value={
          <Link
            href={item.source_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            {item.source_url}
          </Link>
        }
      />
    )}
  </>
);
