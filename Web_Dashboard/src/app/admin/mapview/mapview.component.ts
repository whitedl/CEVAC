import { Component, OnInit } from '@angular/core';
import { MapdataService } from '@services/mapdata.service';

@Component({
  selector: 'app-mapview',
  templateUrl: './mapview.component.html',
  styleUrls: ['./mapview.component.scss']
})
export class MapviewComponent implements OnInit {
  showOthers = true;
  map;

  constructor(private loadGISService: MapdataService) {}

  ngOnInit() {
    this.map = this.loadGISService.getMap();
  }
}
