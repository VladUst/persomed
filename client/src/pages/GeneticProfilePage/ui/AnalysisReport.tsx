import { useId, useRef, useState, type ReactNode } from "react";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import type { GeneReport } from "../api/genes";
import type { EvidenceRef, ReportDetail } from "../model/report";
import { ClinvarTab } from "./ClinvarTab";
import { GenotypeRulesTab } from "./GenotypeRulesTab";
import { OverviewTab } from "./OverviewTab";
import { PolygenicScoresTab } from "./PolygenicScoresTab";
import { ReportDetailDialog } from "./ReportDetailDialog";
import { ReportMetadataTab } from "./ReportMetadataTab";

const ReportTabPanel = ({
  children,
  id,
  index,
  value,
}: {
  children: ReactNode;
  id: string;
  index: number;
  value: number;
}) => (
  <Box
    role="tabpanel"
    hidden={value !== index}
    id={`${id}-panel-${index}`}
    aria-labelledby={`${id}-tab-${index}`}
    sx={{ p: { xs: 2, md: 3 } }}
  >
    {value === index && children}
  </Box>
);

export const AnalysisReport = ({ report }: { report: GeneReport }) => {
  const id = useId();
  const [tab, setTab] = useState(0);
  const [detail, setDetail] = useState<ReportDetail | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const pgsTabRef = useRef<HTMLDivElement>(null);
  const clinvarItems = report.clinvar.items ?? [];
  const ruleItems = report.genotype_rules.items ?? [];
  const pgsItems = report.polygenic_scores.items ?? [];

  const openDetail = (nextDetail: ReportDetail) => {
    setDetail(nextDetail);
    setDetailOpen(true);
  };
  const showAllPgs = () => {
    setTab(3);
    requestAnimationFrame(() => pgsTabRef.current?.focus());
  };
  const openEvidence = (ref: EvidenceRef) => {
    if (ref.section === "clinvar") {
      const item = clinvarItems.find((entry) => entry.id === ref.item_id);
      if (item) openDetail({ kind: "clinvar", item });
    } else if (ref.section === "genotype_rules") {
      const item = ruleItems.find((entry) => entry.id === ref.item_id);
      if (item) openDetail({ kind: "rule", item });
    } else {
      const item = pgsItems.find((entry) => entry.pgs_id === ref.item_id);
      if (item) openDetail({ kind: "pgs", item });
    }
  };

  const tabProps = (index: number) => ({
    id: `${id}-tab-${index}`,
    "aria-controls": `${id}-panel-${index}`,
  });

  return (
    <Stack spacing={2}>
      <Paper variant="outlined" sx={{ borderRadius: 3, overflow: "hidden" }}>
        <Tabs
          value={tab}
          onChange={(_, value: number) => setTab(value)}
          variant="scrollable"
          scrollButtons="auto"
          aria-label="Разделы генетического отчёта"
        >
          <Tab label="Обзор" {...tabProps(0)} />
          <Tab
            label={`Классификации ClinVar (${clinvarItems.length})`}
            {...tabProps(1)}
          />
          <Tab
            label={`Проверенные генотипы (${ruleItems.length})`}
            {...tabProps(2)}
          />
          <Tab
            ref={pgsTabRef}
            label={`Полигенные оценки (${pgsItems.length})`}
            {...tabProps(3)}
          />
          <Tab label="Источники" {...tabProps(4)} />
        </Tabs>
        <Divider />
        <ReportTabPanel id={id} value={tab} index={0}>
          <OverviewTab
            report={report}
            onOpen={openDetail}
            onOpenEvidence={openEvidence}
            onShowAllPgs={showAllPgs}
          />
        </ReportTabPanel>
        <ReportTabPanel id={id} value={tab} index={1}>
          <ClinvarTab report={report} onOpen={openDetail} />
        </ReportTabPanel>
        <ReportTabPanel id={id} value={tab} index={2}>
          <GenotypeRulesTab report={report} onOpen={openDetail} />
        </ReportTabPanel>
        <ReportTabPanel id={id} value={tab} index={3}>
          <PolygenicScoresTab report={report} onOpen={openDetail} />
        </ReportTabPanel>
        <ReportTabPanel id={id} value={tab} index={4}>
          <ReportMetadataTab report={report} />
        </ReportTabPanel>
      </Paper>
      <ReportDetailDialog
        detail={detail}
        open={detailOpen}
        onClose={() => setDetailOpen(false)}
      />
    </Stack>
  );
};
