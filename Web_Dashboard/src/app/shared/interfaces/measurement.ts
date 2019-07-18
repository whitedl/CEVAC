export interface Measurement {
  name: string;
  propertyName: string;
  category: string;
  unit: string;
  form: 'AVG' | 'SUM' | 'MIN' | 'MAX';
  display: boolean;
  active: boolean;
  subMeasures?: Measurement[];
}
