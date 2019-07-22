import { Component, OnInit } from '@angular/core';
import { ParamMap, ActivatedRoute } from '@angular/router';
import { MapdataService } from '@services/mapdata.service';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-building-detail',
  templateUrl: './building-detail.component.html',
  styleUrls: ['./building-detail.component.scss']
})
export class BuildingDetailComponent implements OnInit {
  building$!: { [index: string]: any };

  constructor(
    private route: ActivatedRoute,
    private mapdataService: MapdataService
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(
      (params: ParamMap) =>
        (this.building$ = this.mapdataService.getBuilding(params.get('bldg')))
    );
  }
}
