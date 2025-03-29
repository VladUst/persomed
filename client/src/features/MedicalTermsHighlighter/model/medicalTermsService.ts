import type { MedicalTerm } from "./types";

// Mock UMLS database with medical terms
const medicalTermsDatabase: Record<
  string,
  Omit<MedicalTerm, "position" | "id" | "term">
> = {
  гипертония: {
    cui: "C0020538",
    name: "Гипертония",
    canonicalName: "Hypertension",
    type: "Заболевание",
    icd10Code: "I10",
  },
  "артериальная гипертензия": {
    cui: "C0020538",
    name: "Артериальная гипертензия",
    canonicalName: "Arterial hypertension",
    type: "Заболевание",
    icd10Code: "I10",
  },
  "головные боли": {
    cui: "C0018681",
    name: "Головная боль",
    canonicalName: "Headache",
    type: "Симптом",
    icd10Code: "R51",
  },
  сердцебиение: {
    cui: "C0030252",
    name: "Сердцебиение",
    canonicalName: "Palpitation",
    type: "Симптом",
  },
  "повышенное давление": {
    cui: "C0020538",
    name: "Повышенное артериальное давление",
    canonicalName: "High blood pressure",
    type: "Симптом",
    icd10Code: "I10",
  },
  усталость: {
    cui: "C0015672",
    name: "Утомляемость",
    canonicalName: "Fatigue",
    type: "Симптом",
    icd10Code: "R53",
  },
  стресс: {
    cui: "C0038435",
    name: "Психологический стресс",
    canonicalName: "Psychological stress",
    type: "Симптом",
  },
  "гипертрофия левого желудочка": {
    cui: "C3484382",
    name: "Гипертрофия левого желудочка",
    canonicalName: "Left ventricular hypertrophy",
    type: "Состояние",
    icd10Code: "I51.7",
  },
  холестерин: {
    cui: "C0008377",
    name: "Холестерин",
    canonicalName: "Cholesterol",
    type: "Вещество",
  },
};

// List of medical terms to detect
const medicalTermsList = Object.keys(medicalTermsDatabase);

// Find all medical terms in the text
export const findMedicalTerms = (text: string): MedicalTerm[] => {
  const terms: MedicalTerm[] = [];
  const lowerText = text.toLowerCase();

  medicalTermsList.forEach((term) => {
    let startIndex = 0;
    let foundIndex = lowerText.indexOf(term, startIndex);

    while (foundIndex !== -1) {
      const termInfo = medicalTermsDatabase[term];

      terms.push({
        id: `${term}-${foundIndex}`,
        term: text.substring(foundIndex, foundIndex + term.length),
        position: {
          start: foundIndex,
          end: foundIndex + term.length,
        },
        ...termInfo,
      });

      startIndex = foundIndex + term.length;
      foundIndex = lowerText.indexOf(term, startIndex);
    }
  });

  // Sort terms by start position
  return terms.sort((a, b) => a.position.start - b.position.start);
};

// Get details for a medical term
export const getMedicalTermDetails = (
  termId: string,
): MedicalTerm | undefined => {
  const terms = Object.entries(medicalTermsDatabase);
  const term = terms.find(([key]) => termId.startsWith(key));

  if (term) {
    const [termText, info] = term;
    return {
      id: termId,
      term: termText,
      position: { start: 0, end: 0 }, // Placeholder
      ...info,
    };
  }

  return undefined;
};
