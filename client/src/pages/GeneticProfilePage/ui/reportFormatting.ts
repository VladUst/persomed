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
