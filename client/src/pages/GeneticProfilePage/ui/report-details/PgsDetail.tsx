import type { ComponentProps } from "react";
import Divider from "@mui/material/Divider";
import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";
import type { PolygenicScoreItem } from "../../model/report";
import { formatNumber, resultStatus } from "../reportFormatting";
import { Field } from "./DetailFields";

const PgsField = (props: ComponentProps<typeof Field>) => (
  <Field {...props} labelWidth={300} />
);

const hints = {
  coverage:
    "Доля SNP модели, для которых в VCF найден генотип пациента и совпадают координата и аллели. В скобках указано число таких SNP из общего числа SNP модели.",
  score:
    "Сумма вкладов SNP модели: число копий учитываемого аллеля умножается на вес этого SNP. Для части отсутствующих генотипов вместо числа копий используется среднее значение по частоте аллеля.",
  comparisonStatus:
    "Показывает, удалось ли сравнить балл пациента с баллами участников референсной группы EUR.",
  comparisonReason:
    "Причина, по которой сравнение с референсной группой не выполнено.",
  population:
    "Группа EUR из проекта 1000 Genomes, чьи генотипы используются для сравнения баллов.",
  samples:
    "Число участников референсной группы, с баллами которых сравнивается балл пациента.",
  referenceCoverage:
    "Доля SNP модели, найденных и у пациента, и в референсе, от числа SNP модели, доступных в референсе.",
  percentile:
    "Положение балла пациента среди баллов участников группы EUR при расчёте по одним и тем же SNP. Значение 80 означает, что балл выше примерно 80% баллов в этой группе.",
  position:
    "Категория положения балла по шкале перцентилей. Например, «Очень высокое» соответствует 95-му перцентилю и выше.",
  zScore:
    "На сколько стандартных отклонений балл пациента отличается от среднего балла в группе EUR. Положительное значение — выше среднего, отрицательное — ниже.",
};

export const PgsDetail = ({ item }: { item: PolygenicScoreItem }) => {
  const comparison = item.reference_comparison;
  const referenceCoverage =
    comparison.patient_snps != null &&
    comparison.reference_snps != null &&
    comparison.reference_snps > 0
      ? `${formatNumber((comparison.patient_snps / comparison.reference_snps) * 100)}% (совпало ${comparison.patient_snps} из ${comparison.reference_snps})`
      : null;

  return (
    <>
      <PgsField label="Модель" value={item.pgs_id} />
      <PgsField label="Заболевание" value={item.trait} />
      <PgsField label="Статус" value={resultStatus(item.status)} />
      {item.coverage && (
        <>
          <Divider sx={{ my: 1 }} />
          <Typography variant="subtitle2" sx={{ fontWeight: "normal" }}>
            Покрытие модели
          </Typography>
          <PgsField
            label="Покрытие"
            value={`${formatNumber(item.coverage.measured_percent)}% (совпало ${item.coverage.matched} из ${item.coverage.total})`}
            hint={hints.coverage}
          />
          <PgsField
            label="Полигенный балл"
            value={
              item.raw_score == null ? null : formatNumber(item.raw_score, 5)
            }
            hint={hints.score}
          />
        </>
      )}
      <Divider sx={{ my: 1 }} />
      <Typography variant="subtitle2" sx={{ fontWeight: "normal" }}>
        Сравнение с референсом
      </Typography>
      <PgsField
        label="Статус сравнения"
        value={resultStatus(comparison.status)}
        hint={hints.comparisonStatus}
      />
      {comparison.reason && (
        <PgsField
          label="Причина"
          value={comparison.reason.message}
          hint={hints.comparisonReason}
        />
      )}
      <PgsField
        label="Популяция"
        value={comparison.population}
        hint={hints.population}
      />
      <PgsField
        label="Образцы"
        value={comparison.sample_count}
        hint={hints.samples}
      />
      <PgsField
        label="Покрытие относительно референса"
        value={referenceCoverage}
        hint={hints.referenceCoverage}
      />
      <PgsField
        label="EUR-перцентиль"
        value={
          comparison.percentile == null
            ? null
            : formatNumber(comparison.percentile)
        }
        hint={hints.percentile}
      />
      <PgsField
        label="Положение относительно популяции"
        value={comparison.category_label ?? comparison.category}
        hint={hints.position}
      />
      <PgsField
        label="Z-оценка"
        value={
          comparison.z_score == null
            ? null
            : formatNumber(comparison.z_score, 2)
        }
        hint={hints.zScore}
      />
      {item.research_effect && (
        <>
          <Divider sx={{ my: 1 }} />
          <Typography variant="subtitle2" sx={{ fontWeight: "normal" }}>
            Исследовательская оценка, не абсолютный риск
          </Typography>
          <PgsField
            label="HR и интервал"
            value={`${formatNumber(item.research_effect.value, 2)} (${formatNumber(item.research_effect.range.lower, 2)}–${formatNumber(item.research_effect.range.upper, 2)})`}
          />
          <PgsField label="Исход" value={item.research_effect.outcome} />
          <PgsField
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
      <PgsField
        label="Ссылка на модель"
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
    </>
  );
};
