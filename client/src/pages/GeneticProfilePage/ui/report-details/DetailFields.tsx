import type { ReactNode } from "react";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import type { Source } from "../../model/report";

export const Field = ({
  label,
  value,
}: {
  label: string;
  value: ReactNode;
}) => (
  <Box
    sx={{
      display: "grid",
      gridTemplateColumns: { xs: "1fr", sm: "180px 1fr" },
      gap: 1,
      py: 0.75,
    }}
  >
    <Typography variant="body2" color="text.secondary">
      {label}
    </Typography>
    <Typography
      component="div"
      variant="body2"
      sx={{ overflowWrap: "anywhere" }}
    >
      {value ?? "Нет данных"}
    </Typography>
  </Box>
);

export const Sources = ({ sources }: { sources: Source[] }) => (
  <Stack spacing={1}>
    {sources.map((source, index) => (
      <Box key={`${source.url}-${index}`}>
        <Link
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          sx={{ overflowWrap: "anywhere" }}
        >
          {source.citation ?? source.reference ?? source.url}
        </Link>
        {source.citation && source.citation !== source.url && (
          <Typography variant="caption" sx={{ display: "block" }}>
            {source.url}
          </Typography>
        )}
        {source.doi && (
          <Typography variant="caption" sx={{ display: "block" }}>
            DOI: {source.doi}
          </Typography>
        )}
        {source.pubmed && (
          <Typography variant="caption" sx={{ display: "block" }}>
            PubMed: {source.pubmed}
          </Typography>
        )}
        {source.reference && source.citation && (
          <Typography variant="caption" sx={{ display: "block" }}>
            {source.reference}
          </Typography>
        )}
      </Box>
    ))}
  </Stack>
);
