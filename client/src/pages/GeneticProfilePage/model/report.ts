import type { components } from "@/shared/api";

export type Finding = components["schemas"]["Finding"];
export type ClinvarItem = components["schemas"]["ClinvarItem"];
export type GenotypeRuleItem = components["schemas"]["GenotypeRuleItem"];
export type PolygenicScoreItem = components["schemas"]["PolygenicScoreItem"];
export type Source = components["schemas"]["Source"];
export type EvidenceRef = components["schemas"]["EvidenceRef"];

const dateFormatter = new Intl.DateTimeFormat("ru-RU", {
  dateStyle: "medium",
  timeStyle: "short",
});

export const formatDateTime = (value: string) =>
  dateFormatter.format(new Date(value));

export const formatNumber = (value: number, digits = 1) =>
  new Intl.NumberFormat("ru-RU", {
    maximumFractionDigits: digits,
  }).format(value);

export const formatBytes = (value: number) =>
  value < 1024 * 1024
    ? `${formatNumber(value / 1024)} КБ`
    : `${formatNumber(value / (1024 * 1024))} МБ`;

export const resultStatus = (status: string) =>
  status === "evaluated" ? "Оценено" : "Не оценено";

const stabilityQualityLabels: Record<string, string> = {
  good: "Хорошая",
  limited: "Ограниченная",
  low: "Низкая",
};

export const stabilityQuality = (quality?: string | null) =>
  quality ? (stabilityQualityLabels[quality] ?? quality) : "—";
