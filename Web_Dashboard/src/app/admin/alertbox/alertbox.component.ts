import { Component, OnInit } from '@angular/core';
import { AlertService } from '@app/alert.service';
import { Alert } from '@app/alert';

@Component({
  selector: 'app-alertbox',
  templateUrl: './alertbox.component.html',
  styleUrls: ['./alertbox.component.scss']
})
export class AlertboxComponent implements OnInit {
  alerts: Alert[] = [];

  constructor(private alertService: AlertService) {}

  ngOnInit() {
    this.getAlerts();
  }

  getAlerts(): void {
    this.alertService.getAlerts().subscribe(alerts => (this.alerts = alerts));
  }
}
