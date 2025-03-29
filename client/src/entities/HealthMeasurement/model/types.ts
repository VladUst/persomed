export interface HealthMeasurementData {
  id: string;
  canonicalName?: string;
  name: string;
  value?: string;
  unit?: string;
  date?: string;
  targetReached?: boolean;
  targetLevelMin?: number;
  targetLevelMax?: number;
}
