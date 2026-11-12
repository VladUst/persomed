import type { ReactNode } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Divider from "@mui/material/Divider";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import type {
  ClinvarItem,
  Finding,
  GenotypeRuleItem,
  PolygenicScoreItem,
  Source,
} from "../model/report";
import { formatNumber, resultStatus, stabilityQuality } from "../model/report";

export type ReportDetail =
  | { kind: "finding"; item: Finding }
  | { kind: "clinvar"; item: ClinvarItem }
  | { kind: "rule"; item: GenotypeRuleItem }
  | { kind: "pgs"; item: PolygenicScoreItem };

const Field = ({ label, value }: { label: string; value: ReactNode }) => (
  <Box
    sx={{
      display: "grid",
      gridTemplateColumns: { xs: "1fr", sm: "180px 1fr" },
      gap: 1,
      py: 0.75,
    }}
  >
    <Typography variant="body2" color="text.secondary">
      {label}
    </Typography>
    <Typography
      component="div"
      variant="body2"
      sx={{ overflowWrap: "anywhere" }}
    >
      {value ?? "Нет данных"}
    </Typography>
  </Box>
);

const Sources = ({ sources }: { sources: Source[] }) => (
  <Stack spacing={1}>
    {sources.map((source, index) => (
      <Box key={`${source.url}-${index}`}>
        <Link
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          sx={{ overflowWrap: "anywhere" }}
        >
          {source.citation ?? source.reference ?? source.url}
        </Link>
        {source.citation && source.citation !== source.url && (
          <Typography variant="caption" sx={{ display: "block" }}>
            {source.url}
          </Typography>
        )}
        {source.doi && (
          <Typography variant="caption" sx={{ display: "block" }}>
            DOI: {source.doi}
          </Typography>
        )}
        {source.pubmed && (
          <Typography variant="caption" sx={{ display: "block" }}>
            PubMed: {source.pubmed}
          </Typography>
        )}
        {source.reference && source.citation && (
          <Typography variant="caption" sx={{ display: "block" }}>
            {source.reference}
          </Typography>
        )}
      </Box>
    ))}
  </Stack>
);

const DetailContent = ({ detail }: { detail: ReportDetail }) => {
  if (detail.kind === "finding") {
    const item = detail.item;
    return (
      <>
        <Field label="Гены" value={item.genes.join(", ")} />
        <Field label="Роль находки" value={item.role} />
        <Field label="Интерпретация" value={item.interpretation} />
        <Field label="Вопрос врачу" value={item.clinical_question} />
        <Field label="Следующий шаг" value={item.next_step} />
        <Field label="Ограничения" value={item.limitations.join("; ")} />
        <Field
          label="Ссылки на данные"
          value={item.evidence_refs
            .map((ref) => `${ref.section}: ${ref.item_id}`)
            .join("; ")}
        />
        <Field label="Источники" value={<Sources sources={item.sources} />} />
      </>
    );
  }

  if (detail.kind === "clinvar") {
    const item = detail.item;
    return (
      <>
        <Field label="Гены" value={item.genes.join(", ")} />
        <Field label="Состояния" value={item.conditions.join("; ")} />
        <Field
          label="Вариант"
          value={`${item.variant.genome_build} · chr${item.variant.chromosome}:${item.variant.position} ${item.variant.ref}>${item.variant.alt}`}
        />
        <Field label="rsID" value={item.variant.rsid} />
        <Field label="Генотип" value={`${item.genotype} · ${item.zygosity}`} />
        <Field
          label="Категория"
          value={`${item.significance.label} (${item.category})`}
        />
        <Field
          label="Заключение источника"
          value={item.significance.original}
        />
        <Field label="ClinVar accession" value={item.accession} />
        <Field label="Статус проверки" value={item.review_status} />
        <Field label="Дата оценки" value={item.last_evaluated} />
        {item.source_url && (
          <Field
            label="Запись ClinVar"
            value={
              <Link
                href={item.source_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Открыть источник
              </Link>
            }
          />
        )}
      </>
    );
  }

  if (detail.kind === "rule") {
    const item = detail.item;
    return (
      <>
        <Field label="Гены" value={item.genes.join(", ")} />
        <Field label="Статус" value={resultStatus(item.status)} />
        {item.reason && (
          <Field
            label="Причина пропуска"
            value={`${item.reason.message} (${item.reason.code})`}
          />
        )}
        <Field
          label="Наблюдаемые варианты"
          value={
            item.observed_variants.length
              ? item.observed_variants
                  .map(
                    (variant) =>
                      `${variant.rsid}: ${variant.genotype} [${variant.alleles.join("/")}]${variant.phased ? `, фаза ${variant.phase_set ?? "указана"}` : ", фаза не установлена"}`,
                  )
                  .join("; ")
              : "Нет данных"
          }
        />
        <Field label="Диплотип" value={item.diplotype} />
        {item.result && (
          <>
            <Field
              label="Результат"
              value={`${item.result.label} (${item.result.code})`}
            />
            <Field label="Объяснение" value={item.result.explanation} />
          </>
        )}
        {item.effect && (
          <>
            <Field
              label="Отношение шансов"
              value={`OR ${formatNumber(item.effect.value, 2)} · ${item.effect.context}`}
            />
            <Field
              label="Источники OR"
              value={<Sources sources={item.effect.sources} />}
            />
          </>
        )}
        <Field label="Ограничения" value={item.limitations.join("; ")} />
        <Field label="Источники" value={<Sources sources={item.sources} />} />
      </>
    );
  }

  const item = detail.item;
  const comparison = item.reference_comparison;
  return (
    <>
      <Field label="Модель" value={item.pgs_id} />
      <Field label="Признак" value={`${item.trait} (${item.trait_id})`} />
      <Field label="Статус" value={resultStatus(item.status)} />
      {item.reason && (
        <Field
          label="Примечание"
          value={`${item.reason.message} (${item.reason.code})`}
        />
      )}
      {item.coverage && (
        <>
          <Divider sx={{ my: 1 }} />
          <Typography variant="subtitle2">Покрытие модели</Typography>
          <Field
            label="SNP"
            value={`Всего ${item.coverage.total}; совпало ${item.coverage.matched}; импутировано ${item.coverage.imputed}; пропущено ${item.coverage.skipped}`}
          />
          <Field
            label="Покрытие"
            value={`Измеренное ${formatNumber(item.coverage.measured_percent)}%; эффективное ${formatNumber(item.coverage.effective_percent)}%`}
          />
        </>
      )}
      <Field
        label="Техническая сумма"
        value={item.raw_score == null ? null : formatNumber(item.raw_score, 5)}
      />
      <Divider sx={{ my: 1 }} />
      <Typography variant="subtitle2">Сравнение с референсом</Typography>
      <Field label="Статус" value={resultStatus(comparison.status)} />
      {comparison.reason && (
        <Field
          label="Причина"
          value={`${comparison.reason.message} (${comparison.reason.code})`}
        />
      )}
      <Field label="Популяция" value={comparison.population} />
      <Field label="Образцы" value={comparison.sample_count} />
      <Field
        label="SNP в VCF / референсе"
        value={`${comparison.patient_snps ?? "—"} / ${comparison.reference_snps ?? "—"}`}
      />
      <Field
        label="EUR-перцентиль"
        value={
          comparison.percentile == null
            ? null
            : `${formatNumber(comparison.percentile)}-й`
        }
      />
      <Field
        label="Категория"
        value={comparison.category_label ?? comparison.category}
      />
      <Field
        label="Z-оценка"
        value={
          comparison.z_score == null
            ? null
            : formatNumber(comparison.z_score, 2)
        }
      />
      {item.stability && (
        <>
          <Divider sx={{ my: 1 }} />
          <Typography variant="subtitle2">Устойчивость оценки</Typography>
          <Field
            label="Качество"
            value={stabilityQuality(item.stability.quality)}
          />
          <Field
            label="R² / согласованность"
            value={`${formatNumber(item.stability.r_squared, 2)} / ${formatNumber(item.stability.tier_agreement, 2)}`}
          />
          <Field
            label="Интервал перцентиля"
            value={`${formatNumber(item.stability.percentile_interval.lower)}–${formatNumber(item.stability.percentile_interval.upper)}`}
          />
        </>
      )}
      {item.research_effect && (
        <>
          <Divider sx={{ my: 1 }} />
          <Typography variant="subtitle2">
            Исследовательская оценка, не абсолютный риск
          </Typography>
          <Field
            label="HR и интервал"
            value={`${formatNumber(item.research_effect.value, 2)} (${formatNumber(item.research_effect.range.lower, 2)}–${formatNumber(item.research_effect.range.upper, 2)})`}
          />
          <Field label="Исход" value={item.research_effect.outcome} />
          <Field label="Примечание" value={item.research_effect.note} />
          <Field
            label="Источник"
            value={
              <Link
                href={item.research_effect.source_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Открыть исследование
              </Link>
            }
          />
        </>
      )}
      <Field
        label="PGS Catalog"
        value={
          <Link
            href={item.source_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            Открыть модель
          </Link>
        }
      />
    </>
  );
};

export const ReportDetailDialog = ({
  detail,
  open,
  onClose,
}: {
  detail: ReportDetail | null;
  open: boolean;
  onClose: () => void;
}) => {
  const title =
    detail?.kind === "finding"
      ? detail.item.condition
      : detail?.kind === "clinvar"
        ? detail.item.conditions.join("; ") || "Вариант ClinVar"
        : detail?.kind === "rule"
          ? detail.item.condition
          : (detail?.item.trait ?? "Подробности");

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="md"
      scroll="paper"
    >
      <DialogTitle>{title}</DialogTitle>
      <DialogContent dividers>
        {detail && <DetailContent detail={detail} />}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Закрыть</Button>
      </DialogActions>
    </Dialog>
  );
};
