const significanceLabels: Record<string, string> = {
  pathogenic: "Патогенный",
  "likely pathogenic": "Вероятно патогенный",
  "pathogenic/likely pathogenic": "Патогенный или вероятно патогенный",
  "conflicting interpretations of pathogenicity":
    "Противоречивые оценки патогенности",
  "uncertain significance": "Неопределённая клиническая значимость",
  "risk factor": "Фактор риска",
  association: "Ассоциация",
  affects: "Влияет на признак",
  "drug response": "Связь с ответом на препарат",
};

const reviewStatusLabels: Record<string, string> = {
  "no assertion criteria provided": "Критерии оценки не предоставлены",
  "criteria provided, single submitter":
    "Критерии оценки представлены одним источником",
  "criteria provided, multiple submitters, no conflicts":
    "Критерии оценки представлены; несколько источников, расхождений нет",
  "criteria provided, conflicting interpretations":
    "Критерии оценки представлены; заключения противоречат друг другу",
  "reviewed by expert panel": "Проверено экспертной группой",
  "practice guideline": "Приведено в клинических рекомендациях",
  "no assertion provided": "Заключение не предоставлено",
  "no classification provided": "Классификация не предоставлена",
};

const zygosityLabels: Record<string, string> = {
  heterozygous: "Гетерозиготный",
  homozygous_ref: "Гомозиготный по референсному аллелю",
  homozygous_alt: "Гомозиготный по альтернативному аллелю",
  unknown: "Не определён",
};

const translate = (value: string, labels: Record<string, string>) =>
  labels[value.trim().toLowerCase()] ?? value;

export const clinvarSignificance = (value: string) =>
  translate(value, significanceLabels);

export const clinvarReviewStatus = (value?: string | null) =>
  value ? translate(value, reviewStatusLabels) : "Не указан";

export const clinvarZygosity = (value: string) =>
  translate(value, zygosityLabels);

export const clinvarEvaluationDate = (value?: string | null) =>
  value?.replace(/^(\d{4})-(\d{2})-(\d{2})$/, "$3.$2.$1") ?? null;
