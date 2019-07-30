import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable, Subject, BehaviorSubject } from 'rxjs';
import { shareReplay } from 'rxjs/operators';

import { Alert } from '@shared/interfaces/alert';

@Injectable({
  providedIn: 'root'
})
export class AlertService {
  private buildingAlerts!: [string, Alert[], Alert[]][];
  private buildingAlertsSubject!: Subject<[string, Alert[], Alert[]][]>;
  private alerts!: Alert[];
  private alertsSubject!: BehaviorSubject<Alert[]>;
  private alerts$!: Observable<Alert[]>;
  private alertsUrl = 'http://wfic-cevac1/requests/alerts.php';

  constructor(private http: HttpClient) {
    this.initialize();
  }

  initialize() {
    this.alertsSubject = new BehaviorSubject<Alert[]>([]);
    this.buildingAlertsSubject = new Subject<[string, Alert[], Alert[]][]>();
    this.http.get<Alert[]>(this.alertsUrl).subscribe(response => {
      this.alerts = response;
      this.alertsSubject.next(this.alerts);
    });
    this.alerts$ = this.alertsSubject.asObservable().pipe(shareReplay(1));
  }

  getAlerts(): Observable<Alert[]> {
    return this.alertsSubject;
  }

  removeAlert(alertID: number) {
    this.alerts = this.alerts.filter(v => v.EventID !== alertID);
    this.alertsSubject.next(this.alerts);
  }

  acknowledge(alert: Alert) {
    const options = {
      params: new HttpParams()
        .set('EventID', alert.EventID.toString())
        .set('ACK', '1')
    };
    return this.http.patch(
      'http://wfic-cevac1/requests/acknowledge.php',
      null,
      options
    );
  }
}
