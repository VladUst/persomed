import { CircularProgress, Box } from "@mui/material";
import { memo } from "react";

const PageLoader = () => (
  <Box
    sx={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      width: "100%",
    }}
  >
    <CircularProgress size={80} />
  </Box>
);

export default memo(PageLoader);
