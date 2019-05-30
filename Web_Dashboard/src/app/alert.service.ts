import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Alert } from 'src/app/alert';

@Injectable({
  providedIn: 'root'
})
export class AlertService {
	
	private alertsUrl = 'api/alerts';
	
	constructor(private http: HttpClient) {}

	alerts: Alert[] = [];

	getAlerts(): Observable<Alert[]> {
		return this.http.get<Alert[]>(this.alertsUrl);
	}
  
}
