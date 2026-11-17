import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import type { EvidenceRef, ReportDetail } from "../model/report";
import { ClinvarDetail } from "./report-details/ClinvarDetail";
import { FindingDetail } from "./report-details/FindingDetail";
import { PgsDetail } from "./report-details/PgsDetail";
import { RuleDetail } from "./report-details/RuleDetail";

const DetailContent = ({
  detail,
  onOpenEvidence,
}: {
  detail: ReportDetail;
  onOpenEvidence: (ref: EvidenceRef) => void;
}) => {
  switch (detail.kind) {
    case "finding":
      return (
        <FindingDetail item={detail.item} onOpenEvidence={onOpenEvidence} />
      );
    case "clinvar":
      return <ClinvarDetail item={detail.item} />;
    case "rule":
      return <RuleDetail item={detail.item} />;
    case "pgs":
      return <PgsDetail item={detail.item} />;
  }
};

export const ReportDetailDialog = ({
  detail,
  open,
  onClose,
  onOpenEvidence,
  onBack,
}: {
  detail: ReportDetail | null;
  open: boolean;
  onClose: () => void;
  onOpenEvidence: (ref: EvidenceRef) => void;
  onBack?: () => void;
}) => {
  const title =
    detail?.kind === "finding"
      ? detail.item.condition
      : detail?.kind === "clinvar"
        ? detail.item.conditions.join("; ") || "Вариант ClinVar"
        : detail?.kind === "rule"
          ? detail.item.condition
          : (detail?.item.trait ?? "Подробности");

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="md"
      scroll="paper"
    >
      <DialogTitle>{title}</DialogTitle>
      <DialogContent dividers>
        {detail && (
          <DetailContent detail={detail} onOpenEvidence={onOpenEvidence} />
        )}
      </DialogContent>
      <DialogActions>
        {onBack && <Button onClick={onBack}>Назад</Button>}
        <Button onClick={onClose}>Закрыть</Button>
      </DialogActions>
    </Dialog>
  );
};
