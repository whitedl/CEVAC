import { Component, OnInit } from '@angular/core';
import { MapdataService } from '@services/mapdata.service';

@Component({
  selector: 'app-controlbox',
  templateUrl: './controlbox.component.html',
  styleUrls: ['./controlbox.component.scss']
})
export class ControlboxComponent implements OnInit {
  // define the different views in the MapdataService

  constructor(private mapdataService: MapdataService) {}

  ngOnInit() {}

  update() {
    this.mapdataService.update();
  }
}
