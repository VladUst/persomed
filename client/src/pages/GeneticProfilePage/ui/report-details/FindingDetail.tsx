import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import type { EvidenceRef, Finding } from "../../model/report";
import { Field, Sources } from "./DetailFields";

export const FindingDetail = ({
  item,
  onOpenEvidence,
}: {
  item: Finding;
  onOpenEvidence: (ref: EvidenceRef) => void;
}) => (
  <>
    <Field label="Гены" value={item.genes.join(", ")} />
    <Field label="Заключение" value={item.role} />
    <Field label="Интерпретация" value={item.interpretation} />
    <Field label="Рекомендация" value={item.recommendation} />
    <Field label="Источники" value={<Sources sources={item.sources} />} />
    {item.evidence_refs.length > 0 && (
      <Field
        label="Доказательства"
        value={
          <Stack direction="row" sx={{ gap: 1, flexWrap: "wrap" }}>
            {item.evidence_refs.map((ref, index) => (
              <Button
                key={`${ref.section}-${ref.item_id}`}
                size="small"
                variant="outlined"
                onClick={() => onOpenEvidence(ref)}
              >
                Доказательство
                {item.evidence_refs.length > 1 ? ` ${index + 1}` : ""}
              </Button>
            ))}
          </Stack>
        }
      />
    )}
  </>
);
