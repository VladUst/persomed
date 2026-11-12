import type { Finding } from "../../model/report";
import { Field, Sources } from "./DetailFields";

export const FindingDetail = ({ item }: { item: Finding }) => (
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
