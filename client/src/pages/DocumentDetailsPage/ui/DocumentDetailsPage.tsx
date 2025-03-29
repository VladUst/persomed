import { Page } from "@/widgets/Page";
import { useEffect, useState, useMemo } from "react";
import { useParams } from "react-router-dom";
import cls from "./DocumentDetailsPage.module.scss";
import { Button, Divider } from "@mui/material";
import PlagiarismIcon from "@mui/icons-material/Plagiarism";
import { MedicalTermsHighlighter } from "@/features/MedicalTermsHighlighter";

interface HistoryDocumentDetails {
  title: string;
  meta: HistoryDocumentMeta;
  sections: HistoryDocumentSections;
}

interface HistoryDocumentMeta {
  icdCode: string;
  diagnosisDate: string;
  doctor: string;
  specialty: string;
  nosology: string;
  diseaseType: string;
  clinicName: string;
}

interface HistoryDocumentSections {
  anamnesis: string;
  clinicalFindings: string;
  diagnosis: string;
  treatmentPlan: string;
  conclusion: string;
}

const document: HistoryDocumentDetails = {
  title: "Артериальная гипертензия",
  meta: {
    icdCode: "I10",
    diagnosisDate: "2024-11-20",
    doctor: "Иванов Петр Сергеевич",
    specialty: "Терапевт",
    nosology: "Сердечно-сосудистые заболевания",
    diseaseType: "Хроническое",
    clinicName: "Городская поликлиника №1",
  },
  sections: {
    anamnesis: `
      Пациент обратился с жалобами на периодические головные боли, учащенное сердцебиение, повышенное давление до 160/100 мм рт. ст., ощущение усталости. 
      История болезни: гипертония у пациента диагностирована впервые 5 лет назад. 
      Семейный анамнез отягощен: у отца и матери артериальная гипертензия.
      Обострение состояния отмечается на фоне стрессов и нерегулярного образа жизни.
    `,
    clinicalFindings: `
      При осмотре: артериальное давление - 150/95 мм рт. ст., частота сердечных сокращений - 85 уд./мин.
      Данные ЭКГ: признаки гипертрофии левого желудочка.
      Биохимический анализ крови: повышение уровня холестерина до 6,5 ммоль/л.
      Анализы мочи: без особенностей.
    `,
    diagnosis: `
      Установленный диагноз: Артериальная гипертензия, стадия 2, риск 3.
      Осложнения: гипертрофия левого желудочка.
    `,
    treatmentPlan: `
      - Фармакотерапия:
        1. Лизиноприл 10 мг утром, ежедневно.
        2. Аторвастатин 20 мг на ночь, ежедневно.
        3. Гидрохлортиазид 12,5 мг утром, ежедневно.
      - Диетические рекомендации:
        Ограничение соли до 5 г в сутки, уменьшение потребления насыщенных жиров.
      - Лечебная физкультура:
        Умеренные аэробные нагрузки (30 минут в день, 5 раз в неделю).
      - Контроль состояния:
        Ежедневное измерение артериального давления, повторный визит через месяц.
    `,
    conclusion: `
      На основании клинических данных, анамнеза и результатов лабораторных исследований 
      рекомендована фармакотерапия и изменения образа жизни.
      Необходим постоянный контроль уровня артериального давления и липидного профиля.
    `,
  },
};

const metaKeyMapper: Record<string, string> = {
  icdCode: "Код МКБ",
  diagnosisDate: "Дата постановки",
  doctor: "Врач",
  specialty: "Специальность",
  nosology: "Нозология",
  diseaseType: "Тип заболевания",
  clinicName: "Учреждение",
};

const sectionKeyMapper: Record<string, string> = {
  anamnesis: "Анамнез",
  clinicalFindings: "Клинические данные",
  diagnosis: "Диагноз",
  treatmentPlan: "План лечения",
  conclusion: "Заключение",
};

export const DocumentDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  const [isHighlightingActive, setIsHighlightingActive] = useState(false);

  useEffect(() => {
    console.log(id);
  }, [id]);

  // Convert sections to Record<string, string> for MedicalTermsHighlighter
  const sectionsRecord = useMemo<Record<string, string>>(() => {
    return document.sections as unknown as Record<string, string>;
  }, []);

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

  const toggleHighlighting = () => {
    setIsHighlightingActive((prev) => !prev);
  };

  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>{document.title}</h1>
        <section>{renderMeta()}</section>
        <section className={cls.content}>
          {isHighlightingActive ? (
            <MedicalTermsHighlighter
              sections={sectionsRecord}
              sectionTitles={sectionKeyMapper}
              isActive={isHighlightingActive}
            />
          ) : (
            renderSections()
          )}
        </section>
        <Button
          variant="contained"
          size="large"
          className={cls.button}
          endIcon={<PlagiarismIcon />}
          onClick={toggleHighlighting}
          color={isHighlightingActive ? "secondary" : "primary"}
        >
          {isHighlightingActive ? "Завершить анализ" : "Анализ текста"}
        </Button>
      </article>
    </Page>
  );
};
