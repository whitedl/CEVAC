import { HttpClient } from '@angular/common/http';
import { merge, Observable, of as observableOf } from 'rxjs';
import { catchError, map, startWith, switchMap } from 'rxjs/operators';

import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';

import { Alert } from '@shared/interfaces/alert';

@Component({
  selector: 'app-alertsview',
  templateUrl: './alertsview.component.html',
  styleUrls: ['./alertsview.component.scss']
})
export class AlertsviewComponent implements AfterViewInit {
  displayedColumns: string[] = [
    'EventID',
    'AlertType',
    'BuildingSName',
    'Acknowledged',
    'Resolved',
    'AlertMessage'
  ];
  alerts: Alert[] = [];
  isLoading = false;
  count = 0;

  apiUrl = 'http://wfic-cevac1/api/alerts';

  @ViewChild(MatPaginator, { static: false }) paginator!: MatPaginator;
  @ViewChild(MatSort, { static: false }) sort!: MatSort;

  constructor(private http: HttpClient) {}

  getAlerts(): Observable<Alert[]> {
    return this.http.get<Alert[]>(this.apiUrl);
  }

  ngAfterViewInit() {
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));

    merge(this.sort.sortChange, this.paginator.page)
      .pipe(
        startWith({}),
        switchMap(() => {
          this.isLoading = true;
          return this.getAlerts();
        }),
        map(alerts => {
          this.isLoading = false;
          this.count = alerts.length;
          console.log(typeof alerts);
          return alerts;
        }),
        catchError(() => {
          this.isLoading = false;
          return observableOf([]);
        })
      )
      .subscribe(alerts => (this.alerts = alerts));
  }
}
