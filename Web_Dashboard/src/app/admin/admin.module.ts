import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MaterialModule } from '@app/material.module';

import { AdminRoutingModule } from './admin-routing.module';

import { MapviewComponent } from './mapview/mapview.component';
import { AlertboxComponent } from './alertbox/alertbox.component';

@NgModule({
  declarations: [MapviewComponent, AlertboxComponent],
  imports: [CommonModule, MaterialModule, AdminRoutingModule]
})
export class AdminModule {}
