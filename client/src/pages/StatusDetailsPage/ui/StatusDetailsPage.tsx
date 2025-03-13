import { Page } from "@/widgets/Page";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import cls from "./StatusDetailsPage.module.scss";
import { Button, Divider } from "@mui/material";
import { RateForm } from "@/features/PatientStatusInfo";

const riskFactors = [
  {
    name: "High risk of heart attack",
    source: "Heart attack risk assessment model. Accuracy: 95%",
    date: "2024-11-15",
  },
  {
    name: "Target blood pressure not achieved",
    source: "Health indicator dynamics assessment",
    date: "2024-11-18",
  },
  {
    name: "Target heart rate not achieved",
    source: "Health indicator dynamics assessment",
    date: "2024-11-20",
  },
  {
    name: "Arterial hypertension",
    source: "Chronic condition from medical history",
    date: "2024-11-12",
  },
  {
    name: "Heart failure",
    source: "Chronic condition from medical history",
    date: "2024-11-19",
  },
];

export const StatusDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  useEffect(() => {
    console.log(id);
  }, [id]);

  const [isRateFormOpen, setIsRateFormOpen] = useState(false);

  const showRateForm = () => {
    setIsRateFormOpen(true);
  };

  const closeRateForm = () => {
    setIsRateFormOpen(false);
  };

  if (id === "3") {
    return (
      <Page>
        <article className={cls.document}>
          <h1 className={cls.title}>Risk Assessment</h1>
          <section className={cls.content}>
            <div>
              <Divider textAlign="left" className={cls.divider}>
                Cardiovascular Diseases
              </Divider>
              <p>
                <span className={cls.sectionLabel}>Risk Level:</span> High
              </p>
              <p>
                <span className={cls.sectionLabel}>Source:</span> Cardiovascular
                Disease Risk Assessment Model
              </p>
              <p>
                <span className={cls.sectionLabel}>Assessment Date:</span>{" "}
                2024-11-15
              </p>
              <Button
                className={cls.btn}
                onClick={showRateForm}
                variant="outlined"
                size="large"
              >
                Manual Assessment
              </Button>
              <RateForm
                isOpen={isRateFormOpen}
                onClose={closeRateForm}
                title="Cardiovascular Diseases"
                defaultValue={75}
              />
            </div>
            <div>
              <Divider textAlign="left" className={cls.divider}>
                Digestive System Diseases
              </Divider>
              <p>
                <span className={cls.sectionLabel}>Risk Level:</span> Medium
              </p>
              <p>
                <span className={cls.sectionLabel}>Source:</span> Manual
                Assessment. Justification: Consistently high level of
                gallbladder dysfunction, accompanied by...
              </p>
              <p>
                <span className={cls.sectionLabel}>Assessment Date:</span>{" "}
                2024-11-15
              </p>
              <Button
                className={cls.btn}
                onClick={showRateForm}
                variant="outlined"
                size="large"
              >
                Manual Assessment
              </Button>
            </div>
            <div>
              <Divider textAlign="left" className={cls.divider}>
                Respiratory Diseases
              </Divider>
              <p>
                <span className={cls.sectionLabel}>Risk Level:</span> Low
              </p>
              <p>
                <span className={cls.sectionLabel}>Source:</span> Manual
                Assessment. Justification: ...
              </p>
              <p>
                <span className={cls.sectionLabel}>Assessment Date:</span>{" "}
                2024-11-15
              </p>
              <Button
                className={cls.btn}
                onClick={showRateForm}
                variant="outlined"
                size="large"
              >
                Manual Assessment
              </Button>
            </div>
          </section>
        </article>
      </Page>
    );
  }

  const renderRiskFactors = () =>
    riskFactors.map((factor, index) => (
      <div key={index}>
        <Divider textAlign="left" className={cls.divider}>
          {factor.name}
        </Divider>
        <p>
          <span className={cls.sectionLabel}>Source:</span> {factor.source}
        </p>
        <p>
          <span className={cls.sectionLabel}>Date:</span> {factor.date}
        </p>
      </div>
    ));

  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>Risk Factors</h1>
        <section className={cls.content}>{renderRiskFactors()}</section>
      </article>
    </Page>
  );
};
