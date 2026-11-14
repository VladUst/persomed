import type { ReactNode } from "react";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Link from "@mui/material/Link";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import type { Source } from "../../model/report";

export const Field = ({
  label,
  value,
  hint,
  labelWidth = 180,
}: {
  label: string;
  value: ReactNode;
  hint?: string;
  labelWidth?: number;
}) => (
  <Box
    sx={{
      display: "grid",
      gridTemplateColumns: {
        xs: "1fr",
        sm: `${labelWidth}px minmax(0, 1fr)`,
      },
      gap: 1,
      py: 0.75,
    }}
  >
    <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
      <Typography
        variant="body2"
        color="text.secondary"
        sx={hint ? { whiteSpace: { sm: "nowrap" } } : undefined}
      >
        {label}
      </Typography>
      {hint && (
        <Tooltip
          title={hint}
          arrow
          describeChild
          enterTouchDelay={0}
          leaveTouchDelay={5000}
          slotProps={{
            tooltip: {
              sx: {
                fontSize: "0.8125rem",
                lineHeight: 1.5,
                maxWidth: "min(380px, calc(100vw - 32px))",
                px: 1.25,
                py: 1,
              },
            },
          }}
        >
          <IconButton
            aria-label={`Пояснение: ${label}`}
            sx={{ width: 32, height: 32, flexShrink: 0 }}
          >
            <InfoOutlinedIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      )}
    </Box>
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
