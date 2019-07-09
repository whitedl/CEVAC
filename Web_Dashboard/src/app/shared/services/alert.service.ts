import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Alert } from '@app/alert';

@Injectable({
  providedIn: 'root'
})
export class AlertService {
  private alerts$!: Observable<Alert[]>;
  private alertsUrl = 'http://wfic-cevac1/requests/alerts.php';

  constructor(private http: HttpClient) {
    this.initialize();
  }

  initialize() {
    this.alerts$ = this.http.get<Alert[]>(this.alertsUrl);
  }

  getAlerts(): Observable<Alert[]> {
    return this.alerts$;
  }
}
