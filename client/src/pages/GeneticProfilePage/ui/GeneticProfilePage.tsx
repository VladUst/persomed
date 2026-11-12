import { useState, type ChangeEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { Page } from "@/widgets/Page";
import {
  analysisQueryKey,
  getGeneAnalysis,
  getGeneProfile,
  PATIENT_ID,
  profileQueryKey,
  uploadGeneProfile,
} from "../api/genes";
import { formatBytes, formatDateTime } from "../model/report";
import { AnalysisReport } from "./AnalysisReport";

export const GeneticProfilePage = () => {
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

  return (
    <Page>
      <Box sx={{ maxWidth: 1260, mx: "auto", pb: 6 }}>
        <Stack spacing={1} sx={{ mb: 3 }}>
          <Typography
            variant="overline"
            sx={{ color: "primary.main", fontWeight: 700 }}
          >
            PersoMed · пациент № {PATIENT_ID}
          </Typography>
          <Typography component="h1" variant="h4" sx={{ fontWeight: 800 }}>
            Генетический профиль
          </Typography>
          <Typography color="text.secondary">
            Врачебный разбор VCF с находками, доказательствами и ограничениями
            анализа.
          </Typography>
        </Stack>

        {profileQuery.isPending && (
          <CircularProgress aria-label="Загрузка профиля" />
        )}
        {profileQuery.isError && (
          <Alert
            severity="error"
            sx={{ mb: 3 }}
            action={
              <Button
                color="inherit"
                onClick={() => {
                  profileQuery.refetch().catch(() => undefined);
                }}
              >
                Повторить
              </Button>
            }
          >
            Не удалось получить профиль: {profileQuery.error.message}
          </Alert>
        )}

        {!profileQuery.isError && !profileQuery.isPending && (
          <>
            <Paper
              variant="outlined"
              sx={{ p: { xs: 2, md: 3 }, mb: 3, borderRadius: 3 }}
            >
              <Stack spacing={2}>
                <Stack
                  direction={{ xs: "column", md: "row" }}
                  sx={{ gap: 1, justifyContent: "space-between" }}
                >
                  <Box>
                    <Typography variant="h6" sx={{ fontWeight: 700 }}>
                      Текущий файл генетического профиля
                    </Typography>
                    <Typography
                      variant="body1"
                      sx={{ overflowWrap: "anywhere" }}
                    >
                      {profile?.filename ?? "Профиль пока не загружен"}
                    </Typography>
                  </Box>
                  {profile && (
                    <Chip
                      label={profile.genome_build}
                      color="primary"
                      variant="outlined"
                    />
                  )}
                </Stack>
                {profile && (
                  <Stack direction="row" sx={{ gap: 3, flexWrap: "wrap" }}>
                    <Typography variant="body2">
                      Размер: {formatBytes(profile.size_bytes)}
                    </Typography>
                    <Typography variant="body2">
                      Загружен: {formatDateTime(profile.uploaded_at)}
                    </Typography>
                    {analysisQuery.data && (
                      <Typography variant="body2">
                        Отчёт сформирован:{" "}
                        {formatDateTime(analysisQuery.data.generated_at)}
                      </Typography>
                    )}
                  </Stack>
                )}
                <Stack
                  direction={{ xs: "column", sm: "row" }}
                  sx={{ gap: 2, alignItems: { sm: "center" } }}
                >
                  <Button component="label" variant="outlined">
                    Выбрать файл профиля
                    <input
                      type="file"
                      accept=".vcf"
                      hidden
                      onChange={onSelectFile}
                    />
                  </Button>
                  {selectedFile && (
                    <Typography
                      variant="body2"
                      sx={{ overflowWrap: "anywhere", flex: 1 }}
                    >
                      {selectedFile.name}
                    </Typography>
                  )}
                  <Button
                    variant="contained"
                    disabled={
                      !selectedFile ||
                      Boolean(fileError) ||
                      uploadMutation.isPending
                    }
                    onClick={onUpload}
                  >
                    {uploadMutation.isPending
                      ? "Загрузка…"
                      : profile
                        ? "Заменить профиль"
                        : "Загрузить профиль"}
                  </Button>
                </Stack>
                {fileError && <Alert severity="error">{fileError}</Alert>}
                {uploadMutation.isError && (
                  <Alert severity="error">
                    Не удалось загрузить VCF: {uploadMutation.error.message}
                  </Alert>
                )}
                {uploadMutation.isPending && (
                  <CircularProgress size={24} aria-label="Загрузка файла" />
                )}
              </Stack>
            </Paper>

            {!profile && (
              <Typography variant="body2" color="text.secondary">
                Выберите VCF-файл и загрузите его, чтобы получить анализ.
              </Typography>
            )}
            {profile && analysisQuery.isPending && (
              <Paper variant="outlined" sx={{ p: 4, borderRadius: 3 }}>
                <Stack spacing={2} sx={{ alignItems: "center" }}>
                  <CircularProgress aria-label="Расчёт генетического анализа" />
                  <Typography variant="h6">Формируем анализ</Typography>
                  <Typography
                    color="text.secondary"
                    sx={{ textAlign: "center" }}
                  >
                    Первый расчёт полного VCF может занять значительное время.
                    Оставьте страницу открытой.
                  </Typography>
                </Stack>
              </Paper>
            )}
            {profile && analysisQuery.isError && (
              <Alert
                severity="error"
                action={
                  <Button
                    color="inherit"
                    onClick={() => {
                      analysisQuery.refetch().catch(() => undefined);
                    }}
                  >
                    Повторить
                  </Button>
                }
              >
                Не удалось получить анализ: {analysisQuery.error.message}
              </Alert>
            )}
            {profile && analysisQuery.data && (
              <AnalysisReport report={analysisQuery.data} />
            )}
          </>
        )}
      </Box>

      <Dialog open={confirmReplace} onClose={() => setConfirmReplace(false)}>
        <DialogTitle>Заменить текущий профиль?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            После успешной проверки нового VCF прежний файл и отчёт будут
            удалены. Новый анализ потребуется сформировать заново.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmReplace(false)}>Отмена</Button>
          <Button
            color="warning"
            variant="contained"
            onClick={onConfirmReplace}
          >
            Заменить
          </Button>
        </DialogActions>
      </Dialog>
    </Page>
  );
};
