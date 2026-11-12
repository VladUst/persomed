import type { ChangeEvent } from "react";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import type { GeneProfile } from "../api/genes";
import { formatBytes, formatDateTime } from "./reportFormatting";

export const ProfileCard = ({
  profile,
  generatedAt,
  selectedFile,
  fileError,
  uploadError,
  uploadPending,
  onSelectFile,
  onUpload,
}: {
  profile: GeneProfile | null | undefined;
  generatedAt?: string;
  selectedFile: File | null;
  fileError: string;
  uploadError?: string;
  uploadPending: boolean;
  onSelectFile: (event: ChangeEvent<HTMLInputElement>) => void;
  onUpload: () => void;
}) => (
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
          <Typography variant="body1" sx={{ overflowWrap: "anywhere" }}>
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
          {generatedAt && (
            <Typography variant="body2">
              Отчёт сформирован: {formatDateTime(generatedAt)}
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
          <input type="file" accept=".vcf" hidden onChange={onSelectFile} />
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
          disabled={!selectedFile || Boolean(fileError) || uploadPending}
          onClick={onUpload}
        >
          {uploadPending
            ? "Загрузка…"
            : profile
              ? "Заменить профиль"
              : "Загрузить профиль"}
        </Button>
      </Stack>
      {fileError && <Alert severity="error">{fileError}</Alert>}
      {uploadError && (
        <Alert severity="error">Не удалось загрузить VCF: {uploadError}</Alert>
      )}
      {uploadPending && (
        <CircularProgress size={24} aria-label="Загрузка файла" />
      )}
    </Stack>
  </Paper>
);
