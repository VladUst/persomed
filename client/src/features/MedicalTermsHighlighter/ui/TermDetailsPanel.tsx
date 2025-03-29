import { Paper, Typography, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import type { MedicalTerm } from "../model/types";
import cls from "./MedicalTermsHighlighter.module.scss";
import { classNames } from "@/shared/lib/classNames";

interface TermDetailsPanelProps {
  term: MedicalTerm | null;
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

export const TermDetailsPanel = (props: TermDetailsPanelProps) => {
  const { term, isOpen, onClose, className } = props;

  if (!term) return null;

  return (
    <Paper
      className={classNames(cls.detailsPanel, { [cls.visible]: isOpen }, [
        className,
      ])}
      elevation={3}
    >
      <IconButton
        onClick={onClose}
        className={cls.closeButton}
        size="small"
        color="primary"
      >
        <CloseIcon />
      </IconButton>

      <Typography variant="h6" gutterBottom>
        {term.name}
      </Typography>

      <div className={cls.detailsGrid}>
        <Typography className={cls.label}>Термин:</Typography>
        <Typography>"{term.term}"</Typography>
        <Typography className={cls.label}>Каноническое название:</Typography>
        <Typography>{term.canonicalName}</Typography>
        <Typography className={cls.label}>CUI:</Typography>
        <Typography>{term.cui}</Typography>

        <Typography className={cls.label}>Тип:</Typography>
        <Typography>{term.type}</Typography>

        {term.icd10Code && (
          <>
            <Typography className={cls.label}>Код МКБ-10:</Typography>
            <Typography>{term.icd10Code}</Typography>
          </>
        )}
      </div>
    </Paper>
  );
};
