import { Component, OnInit } from '@angular/core';
import { MapdataService } from '@services/mapdata.service';
import { Measurement } from '@app/shared/interfaces/measurement';
import { debugOutputAstAsTypeScript } from '@angular/compiler';

@Component({
  selector: 'app-controlbox',
  templateUrl: './controlbox.component.html',
  styleUrls: ['./controlbox.component.scss']
})
export class ControlboxComponent implements OnInit {
  // define the different views in the MapdataService
  dataSets: Measurement[] = this.mapdataService.dataSets;
  categories: Set<string> = new Set<string>(this.dataSets.map(v => v.category));

  constructor(private mapdataService: MapdataService) {}

  ngOnInit() {}

  get update() {
    return this.mapdataService.setDataSet();
  }
}
