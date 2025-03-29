export interface MedicalTerm {
  id: string;
  term: string;
  cui: string;
  type: string;
  name: string;
  canonicalName: string;
  icd10Code?: string;
  position: {
    start: number;
    end: number;
  };
}

export interface HighlightedSection {
  id: string;
  title: string;
  text: string;
  terms: MedicalTerm[];
  isHighlightMode: boolean;
}
