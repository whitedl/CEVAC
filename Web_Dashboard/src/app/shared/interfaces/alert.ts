export interface Alert {
  EventID: number;
  AlertType: string;
  AlertMessage?: string;
  Metric?: string;
  BuildingSName: string;
  BuildingDName?: string;
  Acknowledged: number;
  ETDateTime: Date;
  DetectionTimeET: Date;
}
