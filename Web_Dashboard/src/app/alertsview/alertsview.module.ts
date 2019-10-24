import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MaterialModule } from '@app/material.module';

import { AlertsviewRoutingModule } from './alertsview-routing.module';

import { AlertsviewComponent } from './alertsview/alertsview.component';

@NgModule({
  declarations: [AlertsviewComponent],
  imports: [CommonModule, MaterialModule, AlertsviewRoutingModule]
})
export class AlertsviewModule {}
