export interface Alert {
	AlertID: number;
	AlertType: string;
	AlertMessage?: string;
	Metric?: string;
	BLDG: string;
	Acknowledged: number;
	BeginTime: Date;
	EndTime?: Date;
}