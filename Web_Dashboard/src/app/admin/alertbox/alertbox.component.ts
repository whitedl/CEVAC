import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';

import { AlertService } from '@services/alert.service';
import { MapdataService } from '@services/mapdata.service';
import { ColorService } from '@services/color.service';
import { Alert } from '@shared/interfaces/alert';

@Component({
  selector: 'app-alertbox',
  templateUrl: './alertbox.component.html',
  styleUrls: ['./alertbox.component.scss']
})
export class AlertboxComponent implements OnInit {
  alerts$!: Observable<Alert[]>;
  critical$!: Observable<Alert[]>;
  noncritical$!: Observable<Alert[]>;
  buildingAlerts$!: Observable<Map<string, Alert[]>>;

  critD = true;
  noncritD = true;

  constructor(
    private alertService: AlertService,
    private mapdataService: MapdataService,
    private colorService: ColorService
  ) {}

  ngOnInit() {
    this.alerts$ = this.alertService.getAlerts();
    this.critical$ = this.alerts$.pipe(
      map(v => v.filter(alert => alert.AlertType === 'alert'))
    );
    this.noncritical$ = this.alerts$.pipe(
      map(v => v.filter(alert => alert.AlertType === 'warning'))
    );
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
    this.mapdataService.focusBldg(alert.BuildingSName);
  }

  acknowledge(alert: Alert, e: Event) {
    e.stopPropagation();
    this.alertService.acknowledge(alert).subscribe(response => {
      if (response === alert.EventID) {
        this.alertService.removeAlert(response as number);
      } else {
      }
    });
  }
}
