import type { GenotypeRuleItem } from "../../model/report";
import { formatNumber, resultStatus } from "../reportFormatting";
import { Field, Sources } from "./DetailFields";

export const RuleDetail = ({ item }: { item: GenotypeRuleItem }) => (
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
