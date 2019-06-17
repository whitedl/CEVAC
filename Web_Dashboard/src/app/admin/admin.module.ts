import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@app/material.module';

import { AdminRoutingModule } from './admin-routing.module';

import { MapviewComponent } from './mapview/mapview.component';
import { AlertboxComponent } from './alertbox/alertbox.component';
import { ControlboxComponent } from './controlbox/controlbox.component';

@NgModule({
  declarations: [MapviewComponent, AlertboxComponent, ControlboxComponent],
  imports: [CommonModule, MaterialModule, AdminRoutingModule, FormsModule]
})
export class AdminModule {}
