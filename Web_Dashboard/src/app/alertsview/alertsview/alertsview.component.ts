import { HttpClient } from '@angular/common/http';
import { merge, Observable, of as observableOf } from 'rxjs';
import { catchError, map, startWith, switchMap } from 'rxjs/operators';

import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { SelectionModel } from '@angular/cdk/collections';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';

import { Alert } from '@shared/interfaces/alert';
import { MatTable } from '@angular/material/table';

@Component({
  selector: 'app-alertsview',
  templateUrl: './alertsview.component.html',
  styleUrls: ['./alertsview.component.scss']
})
export class AlertsviewComponent implements AfterViewInit {
  displayedColumns: string[] = [
    'select',
    'EventID',
    'AlertType',
    'BuildingSName',
    'Acknowledged',
    'Resolved',
    'AlertMessage',
    'Delete'
  ];
  selection = new SelectionModel<Alert>(true, []);
  alerts: Alert[] = [];
  isLoading = false;
  count = 0;

  apiUrl = 'http://wfic-cevac1/api/alerts';

  @ViewChild(MatTable, { static: false }) table!: MatTable<any>;
  @ViewChild(MatPaginator, { static: false }) paginator!: MatPaginator;
  @ViewChild(MatSort, { static: false }) sort!: MatSort;

  constructor(private http: HttpClient) {}

  deleteRow = (eid: number) => {
    this.http
      .delete<any>(`${this.apiUrl}/${eid}`)
      .subscribe(() => this.getAlerts());
    this.table.renderRows();
  };

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.alerts.length;
    return numSelected === numRows;
  }

  masterToggle() {
    this.isAllSelected()
      ? this.selection.clear()
      : this.alerts.forEach(row => this.selection.select(row));
  }

  getAlerts(): Observable<Alert[]> {
    let requestUrl = `${this.apiUrl}?`;
    if (this.sort.direction) {
      requestUrl += `filter[order]=${this.sort.active} ${this.sort.direction}&`;
    }
    requestUrl += `filter[limit]=${this.paginator.pageSize}&filter[skip]=${this
      .paginator.pageIndex * this.paginator.pageSize}`;
    const countUrl = `${this.apiUrl}/count`;
    this.http.get<any>(countUrl).subscribe(count => (this.count = count.count));
    return this.http.get<Alert[]>(requestUrl);
  }

  ngAfterViewInit() {
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));

    merge(this.sort.sortChange, this.paginator.page)
      .pipe(
        startWith({}),
        switchMap(() => {
          this.isLoading = true;
          this.selection.clear();
          return this.getAlerts();
        }),
        map(alerts => {
          this.isLoading = false;
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
