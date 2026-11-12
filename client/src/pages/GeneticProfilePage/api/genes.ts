import { apiClient, apiError, type components } from "@/shared/api";

export const PATIENT_ID = 1;
const profilePath = "/api/patients/{patient_id}/genes/profile";
const analysisPath = "/api/patients/{patient_id}/genes/analysis";

export type GeneProfile = components["schemas"]["Profile"];
export type GeneReport = components["schemas"]["GeneAnalysisReport"];

export const profileQueryKey = ["genes", PATIENT_ID, "profile"] as const;
export const analysisQueryKey = (profileId: string) =>
  ["genes", PATIENT_ID, "analysis", profileId] as const;

export async function getGeneProfile(signal?: AbortSignal) {
  const { data, error, response } = await apiClient.GET(profilePath, {
    params: { path: { patient_id: PATIENT_ID } },
    signal,
  });
  if (!data) throw apiError(response.status, error);
  return data;
}

export async function getGeneAnalysis(signal?: AbortSignal) {
  const { data, error, response } = await apiClient.GET(analysisPath, {
    params: { path: { patient_id: PATIENT_ID } },
    signal,
  });
  if (!data) throw apiError(response.status, error);
  return data;
}

export async function uploadGeneProfile(file: File) {
  const form = new FormData();
  form.append("file", file);
  const { data, error, response } = await apiClient.POST(profilePath, {
    params: { path: { patient_id: PATIENT_ID } },
    // OpenAPI represents binary form fields as strings; FormData carries the File.
    body: { file: file.name },
    bodySerializer: () => form,
  });
  if (!data) throw apiError(response.status, error);
  return data;
}
