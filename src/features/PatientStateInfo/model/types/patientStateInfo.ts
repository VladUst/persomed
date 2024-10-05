export interface PatientStateItem {
  text: string;
  Icon?: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  label?: string;
}

export type PatientStateInfo = PatientStateItem[];
