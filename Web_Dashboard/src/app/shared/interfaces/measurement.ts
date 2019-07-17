export interface Measurement {
  name: string;
  propertyName: string;
  unit: string;
  form: 'AVG' | 'SUM' | 'MIN' | 'MAX';
  display: boolean;
  active: boolean;
  subMeasures?: Measurement[];
}
