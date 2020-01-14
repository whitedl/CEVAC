import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MapviewComponent } from './mapview/mapview.component';
import { BuildingDetailComponent } from './building-detail/building-detail.component';

const routes: Routes = [
  {
    path: 'map',
    component: MapviewComponent,
    children: [{ path: ':bldg', component: BuildingDetailComponent }]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MapviewRoutingModule {}
