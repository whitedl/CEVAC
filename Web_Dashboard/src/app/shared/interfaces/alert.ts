export interface Alert {
  EventID: number;
  AlertType: string;
  AlertMessage?: string;
  Metric?: string;
  BuildingSName: string;
  BuildingDName?: string;
  Acknowledged: boolean;
  Resolved: boolean;
  ETDateTime: Date;
  DetectionTimeET: Date;
}
