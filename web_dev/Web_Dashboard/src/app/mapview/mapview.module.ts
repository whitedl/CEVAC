import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@app/material.module';

import { MapviewRoutingModule } from './mapview-routing.module';

import { MapviewComponent } from './mapview/mapview.component';
import { AlertboxComponent } from './alertbox/alertbox.component';
import { ControlboxComponent } from './controlbox/controlbox.component';
import { BuildingDetailComponent } from './building-detail/building-detail.component';

@NgModule({
  declarations: [
    MapviewComponent,
    AlertboxComponent,
    ControlboxComponent,
    BuildingDetailComponent
  ],
  imports: [CommonModule, MaterialModule, MapviewRoutingModule, FormsModule]
})
export class MapviewModule {}
