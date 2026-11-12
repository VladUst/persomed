import createClient from "openapi-fetch";
import type { paths } from "./schema";

export const apiClient = createClient<paths>({
  baseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
});

export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message);
  }
}

export const apiError = (status: number, value: unknown): ApiError => {
  if (value && typeof value === "object" && "detail" in value) {
    const detail = value.detail;
    if (typeof detail === "string") return new ApiError(status, detail);
    if (Array.isArray(detail)) {
      return new ApiError(
        status,
        detail
          .map((item) =>
            item && typeof item === "object" && "msg" in item
              ? String(item.msg)
              : "Ошибка проверки данных",
          )
          .join("; "),
      );
    }
  }
  return new ApiError(status, `Ошибка сервера (${status})`);
};
