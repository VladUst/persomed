export interface PatientStateItem {
  text: string;
  Icon?: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  label?: string;
  labelColor?: string;
}

export type PatientStateInfo = PatientStateItem[];
