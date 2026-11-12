import Divider from "@mui/material/Divider";
import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";
import type { PolygenicScoreItem } from "../../model/report";
import {
  formatNumber,
  resultStatus,
  stabilityQuality,
} from "../reportFormatting";
import { Field } from "./DetailFields";

export const PgsDetail = ({ item }: { item: PolygenicScoreItem }) => {
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
