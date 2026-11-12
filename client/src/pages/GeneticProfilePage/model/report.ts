import type { components } from "@/shared/api";

export type Finding = components["schemas"]["Finding"];
export type ClinvarItem = components["schemas"]["ClinvarItem"];
export type GenotypeRuleItem = components["schemas"]["GenotypeRuleItem"];
export type PolygenicScoreItem = components["schemas"]["PolygenicScoreItem"];
export type Source = components["schemas"]["Source"];
export type EvidenceRef = components["schemas"]["EvidenceRef"];

export type ReportDetail =
  | { kind: "finding"; item: Finding }
  | { kind: "clinvar"; item: ClinvarItem }
  | { kind: "rule"; item: GenotypeRuleItem }
  | { kind: "pgs"; item: PolygenicScoreItem };
