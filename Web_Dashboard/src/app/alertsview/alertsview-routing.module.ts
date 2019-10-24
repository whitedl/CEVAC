import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AlertsviewComponent } from './alertsview/alertsview.component';

const routes: Routes = [
  {
    path: 'alerts',
    component: AlertsviewComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AlertsviewRoutingModule {}
