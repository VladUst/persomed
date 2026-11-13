import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
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
import { PATIENT_ID } from "../api/genes";
import { useGeneticProfile } from "../model/useGeneticProfile";
import { AnalysisReport } from "./AnalysisReport";
import { ProfileCard } from "./ProfileCard";

export const GeneticProfilePage = () => {
  const {
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
    closeReplaceDialog,
  } = useGeneticProfile();

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
            <ProfileCard
              profile={profile}
              generatedAt={analysisQuery.data?.generated_at}
              selectedFile={selectedFile}
              fileError={fileError}
              uploadError={
                uploadMutation.isError
                  ? uploadMutation.error.message
                  : undefined
              }
              uploadPending={uploadMutation.isPending}
              onSelectFile={onSelectFile}
              onUpload={onUpload}
            />

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

      <Dialog open={confirmReplace} onClose={closeReplaceDialog}>
        <DialogTitle>Заменить текущий профиль?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            После успешной проверки нового VCF прежний файл и отчёт будут
            удалены. Новый анализ потребуется сформировать заново.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeReplaceDialog}>Отмена</Button>
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
