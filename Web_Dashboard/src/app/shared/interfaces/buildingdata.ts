import { Measurement } from './measurement';

export interface BuildingData {
  metrics: Measurement[];
  [index: string]: any;
}
