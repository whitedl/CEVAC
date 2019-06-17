export interface Alert {
  AlertID: number;
  AlertType: string;
  AlertMessage?: string;
  Metric?: string;
  BLDG_STD: string;
  BLDG_DISP: string;
  Acknowledged: number;
  BeginTime: Date;
  EndTime?: Date;
}
