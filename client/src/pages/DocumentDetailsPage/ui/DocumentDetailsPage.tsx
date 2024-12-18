import { Page } from "@/widgets/Page";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import cls from "./DocumentDetailsPage.module.scss";
import { Button, Divider } from "@mui/material";
import PlagiarismIcon from "@mui/icons-material/Plagiarism";

const document = {
  title: "Arterial Hypertension",
  meta: {
    icdCode: "I10",
    diagnosisDate: "2024-11-20",
    physicianName: "Ivanov Petr Sergeevich",
    specialty: "Therapist",
    nosology: "Cardiovascular Diseases",
    diseaseType: "Chronic",
    clinicName: "City Polyclinic №1",
  },
  sections: {
    anamnesis: `
      The patient presented with complaints of periodic headaches, rapid heartbeat, 
      elevated blood pressure up to 160/100 mmHg, and fatigue. 
      Medical history: hypertension was first diagnosed 5 years ago. 
      Family history is burdened: both father and mother have arterial hypertension.
      Condition exacerbations are noted during periods of stress and irregular lifestyle.
    `,
    clinicalFindings: `
      During examination: blood pressure - 150/95 mmHg, heart rate - 85 bpm.
      ECG data: signs of left ventricular hypertrophy.
      Blood biochemistry: elevated cholesterol level up to 6.5 mmol/L.
      Urine analysis: no abnormalities.
    `,
    diagnosis: `
      Established diagnosis: Arterial hypertension, stage 2, risk 3.
      Complications: left ventricular hypertrophy.
    `,
    treatmentPlan: `
      - Pharmacotherapy:
        1. Lisinopril 10 mg in the morning, daily.
        2. Atorvastatin 20 mg at night, daily.
        3. Hydrochlorothiazide 12.5 mg in the morning, daily.
      - Dietary recommendations:
        Limit salt intake to 5 g per day, reduce consumption of saturated fats.
      - Therapeutic physical exercises:
        Moderate aerobic activities (30 minutes per day, 5 times a week).
      - Condition monitoring:
        Daily blood pressure measurement, follow-up visit in one month.
    `,
    conclusion: `
      Based on clinical data, medical history, and laboratory test results, 
      pharmacotherapy and lifestyle changes are recommended.
      Continuous monitoring of blood pressure and lipid profile is necessary.
    `,
  },
};

const metaKeyMapper: Record<string, string> = {
  icdCode: "ICD Code",
  diagnosisDate: "Diagnosis Date",
  physicianName: "Physician",
  specialty: "Specialty",
  nosology: "Nosology",
  diseaseType: "Disease Type",
  clinicName: "Institution",
};

const sectionKeyMapper: Record<string, string> = {
  anamnesis: "Anamnesis",
  clinicalFindings: "Laboratory tests",
  diagnosis: "Diagnosis",
  treatmentPlan: "Treatment Plan",
  conclusion: "Conclusion",
};

export const DocumentDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  useEffect(() => {
    console.log(id);
  }, [id]);

  const renderMeta = () => (
    <ul>
      {Object.entries(document.meta).map(([key, value]) => (
        <li key={key}>
          <span className={cls.sectionLabel}>
            {metaKeyMapper[key] || key}:{" "}
          </span>
          {value}
        </li>
      ))}
    </ul>
  );

  const renderSections = () =>
    Object.entries(document.sections).map(([key, value]) => (
      <div key={key}>
        <Divider textAlign="left" className={cls.divider}>
          {sectionKeyMapper[key] || key}
        </Divider>
        <p>{value}</p>
      </div>
    ));
  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>{document.title}</h1>
        <section>{renderMeta()}</section>
        <section className={cls.content}>{renderSections()}</section>
        <Button
          variant="contained"
          size="large"
          className={cls.button}
          endIcon={<PlagiarismIcon />}
        >
          Analysis
        </Button>
      </article>
    </Page>
  );
};
