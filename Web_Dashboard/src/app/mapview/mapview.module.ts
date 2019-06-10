import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MaterialModule } from 'src/app/material.module';

import { MapviewRoutingModule } from './mapview-routing.module';

import { MapviewComponent } from './mapview/mapview.component';
import { AlertboxComponent } from './alertbox/alertbox.component';

@NgModule({
  declarations: [
    MapviewComponent,
    AlertboxComponent
  ],
  imports: [
    CommonModule,
    MaterialModule,
    MapviewRoutingModule
  ]
})
export class MapviewModule { }
