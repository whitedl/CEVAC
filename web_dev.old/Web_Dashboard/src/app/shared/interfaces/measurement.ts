export interface Measurement {
  name: string;
  propertyName: string;
  category: string;
  unit: string;
  form: 'avg' | 'sum' | 'min' | 'max';
  display: boolean;
  active: boolean;
  subMeasures?: Measurement[];
}
