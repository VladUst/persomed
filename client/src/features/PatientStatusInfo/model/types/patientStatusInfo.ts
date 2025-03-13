export interface PatientStatusItem {
  text: string;
  Icon?: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  label?: string;
  labelColor?: string;
}

export type PatientStatusInfo = PatientStatusItem[];
