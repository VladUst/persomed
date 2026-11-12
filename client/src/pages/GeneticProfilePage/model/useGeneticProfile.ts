import { useState, type ChangeEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  analysisQueryKey,
  getGeneAnalysis,
  getGeneProfile,
  PATIENT_ID,
  profileQueryKey,
  uploadGeneProfile,
} from "../api/genes";

export const useGeneticProfile = () => {
  const queryClient = useQueryClient();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [confirmReplace, setConfirmReplace] = useState(false);
  const [fileError, setFileError] = useState("");

  const profileQuery = useQuery({
    queryKey: profileQueryKey,
    queryFn: ({ signal }) => getGeneProfile(signal),
  });
  const profile = profileQuery.data?.profile;
  const analysisQuery = useQuery({
    queryKey: analysisQueryKey(profile?.id ?? "none"),
    queryFn: ({ signal }) => getGeneAnalysis(signal),
    enabled: Boolean(profile),
    staleTime: Infinity,
  });
  const uploadMutation = useMutation({
    mutationFn: uploadGeneProfile,
    onSuccess: (result) => {
      queryClient.removeQueries({
        queryKey: ["genes", PATIENT_ID, "analysis"],
      });
      queryClient.setQueryData(profileQueryKey, result);
      setSelectedFile(null);
      setFileError("");
    },
  });

  const onSelectFile = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    event.target.value = "";
    setSelectedFile(file);
    setFileError(
      file && !file.name.toLowerCase().endsWith(".vcf")
        ? "Выберите несжатый файл с расширением .vcf."
        : "",
    );
  };

  const onUpload = () => {
    if (!selectedFile || fileError) return;
    if (profile) setConfirmReplace(true);
    else uploadMutation.mutate(selectedFile);
  };

  const onConfirmReplace = () => {
    setConfirmReplace(false);
    if (selectedFile) uploadMutation.mutate(selectedFile);
  };

  return {
    profile,
    profileQuery,
    analysisQuery,
    uploadMutation,
    selectedFile,
    fileError,
    confirmReplace,
    onSelectFile,
    onUpload,
    onConfirmReplace,
    closeReplaceDialog: () => setConfirmReplace(false),
  };
};
