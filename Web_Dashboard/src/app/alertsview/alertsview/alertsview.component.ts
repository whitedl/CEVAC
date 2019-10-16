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
    'DetectionTimeET',
    'ETDateTime',
    'BuildingSName',
    'AlertMessage',
    'Acknowledged',
    'Resolved',
    'Delete'
  ];
  selection = new SelectionModel<Alert>(true, []);
  alerts: Alert[] = [];
  isLoading = false;

  count = 0;

  // Filters
  buildingNames: string[] = [];
  eventIDs: string[] = [];
  startDate: Date = new Date();
  endDate: Date = new Date();
  ackStatus = 0;
  resStatus = 0;

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

  ackSlideThumb = (val: number) => {
    switch (val) {
      case 0:
        return 'unack';
      case 1:
        return 'both';
      case 2:
        return 'ack';
      default:
        console.log('How did you set the slider to that?');
        return 'something broke';
    }
  };

  resSlideThumb = (val: number) => {
    switch (val) {
      case 0:
        return 'unres';
      case 1:
        return 'both';
      case 2:
        return 'res';
      default:
        console.log('How did you set the slider to that?');
        return 'something broke';
    }
  };

  resetTable = () => {
    this.paginator.pageIndex = 0;
  };

  getAlerts(): Observable<Alert[]> {
    let requestUrl = `${this.apiUrl}?`;
    let countUrl = `${this.apiUrl}/count?`;
    if (this.sort.direction) {
      requestUrl += `filter[order]=${this.sort.active} ${this.sort.direction}&`;
    }
    if (this.ackStatus === 0) {
      requestUrl += `filter[where][Acknowledged]=false&`;
      countUrl += `where[Acknowledged]=false&`;
    } else if (this.ackStatus === 2) {
      requestUrl += `filter[where][Acknowledged]=true&`;
      countUrl += `where[Acknowledged]=true&`;
    }
    if (this.resStatus === 0) {
      requestUrl += `filter[where][Resolved]=false&`;
      countUrl += `where[Resolved]=false&`;
    } else if (this.resStatus === 2) {
      requestUrl += `filter[where][Resolved]=true&`;
      countUrl += `where[Resolved]=true&`;
    }
    requestUrl += `filter[limit]=${this.paginator.pageSize}&filter[skip]=${this
      .paginator.pageIndex * this.paginator.pageSize}`;
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
