import Link from "@mui/material/Link";
import type { ClinvarItem } from "../../model/report";
import { Field } from "./DetailFields";

export const ClinvarDetail = ({ item }: { item: ClinvarItem }) => (
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
    <Field label="Заключение источника" value={item.significance.original} />
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
