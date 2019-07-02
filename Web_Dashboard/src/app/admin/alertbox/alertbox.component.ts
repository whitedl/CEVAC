import { Component, OnInit } from '@angular/core';
import { AlertService } from '@services/alert.service';
import { MapdataService } from '@services/mapdata.service';
import { ColorService } from '@services/color.service';
import { Alert } from '@app/alert';

@Component({
  selector: 'app-alertbox',
  templateUrl: './alertbox.component.html',
  styleUrls: ['./alertbox.component.scss']
})
export class AlertboxComponent implements OnInit {
  alerts: Alert[] = [];

  constructor(
    private alertService: AlertService,
    private mapdataService: MapdataService,
    private colorService: ColorService
  ) {}

  ngOnInit() {
    this.getAlerts();
  }

  getAlertColor(type: string) {
    let col;
    switch (type) {
      case 'alert':
        col = this.colorService.alert;
        break;
      case 'warning':
        col = this.colorService.warn;
        break;
    }
    return {
      color: col
    };
  }

  focus(alert: Alert) {
    this.mapdataService.focusBldg(alert.BLDG_STD);
  }

  alertAll(): Alert[] {
    return this.alerts.filter(alert => alert.AlertID === 1);
  }
  logAl = () => {
    this.alerts[1].AlertID = 3;
  };

  getAlerts(): void {
    this.alertService.getAlerts().subscribe(alerts => (this.alerts = alerts));
  }
}
