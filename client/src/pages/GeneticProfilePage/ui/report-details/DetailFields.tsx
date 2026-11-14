import type { ReactNode } from "react";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
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
  <Box sx={{ display: "grid", gap: 1 }}>
    {sources.map((source, index) => (
      <Link
        key={`${source.url}-${index}`}
        href={source.url}
        target="_blank"
        rel="noopener noreferrer"
        sx={{ overflowWrap: "anywhere" }}
      >
        {source.citation ?? source.url}
      </Link>
    ))}
  </Box>
);
