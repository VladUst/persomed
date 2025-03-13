export interface HealthIndicator {
  id: string;
  name: string;
  value?: string;
  date?: string;
  targetReached?: boolean;
  unit: string;
  targetLevel: [number, number];
}
