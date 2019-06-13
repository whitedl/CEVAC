import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Alert } from '@app/alert';

@Injectable({
  providedIn: 'root'
})
export class AlertService {
  private alertsUrl = 'http://wfic-cevac1/requests/alerts.php';

  constructor(private http: HttpClient) {}

  alerts: Alert[] = [];

  getAlerts(): Observable<Alert[]> {
    return this.http.get<Alert[]>(this.alertsUrl);
  }
}
