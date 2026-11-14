import type { GenotypeRuleItem } from "../../model/report";
import { formatNumber, resultStatus } from "../reportFormatting";
import { Field, Sources } from "./DetailFields";

export const RuleDetail = ({ item }: { item: GenotypeRuleItem }) => (
  <>
    <Field label="Ген" value={item.genes.join(", ")} />
    <Field label="Заболевание или признак" value={item.condition} />
    <Field label="Статус" value={resultStatus(item.status)} />
    {item.reason && (
      <Field label="Причина пропуска" value={item.reason.message} />
    )}
    <Field label="Вариант" value={item.rsids.join(", ")} />
    <Field
      label="Генотип"
      value={
        item.observed_variants.length
          ? item.observed_variants
              .map((variant) =>
                item.rsids.length > 1
                  ? `${variant.rsid}: ${variant.alleles.join("/")}`
                  : variant.alleles.join("/"),
              )
              .join("; ")
          : "Нет данных"
      }
    />
    {item.result && (
      <>
        <Field label="Результат" value={item.result.label} />
        <Field label="Пояснение" value={item.result.explanation} />
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
    <Field label="Источники" value={<Sources sources={item.sources} />} />
  </>
);
