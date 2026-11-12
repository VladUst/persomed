import Typography from "@mui/material/Typography";

export const SectionHeading = ({ title }: { title: string }) => (
  <Typography component="h2" variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
    {title}
  </Typography>
);
