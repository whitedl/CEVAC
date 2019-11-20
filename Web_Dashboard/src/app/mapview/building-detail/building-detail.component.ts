import { Component, OnInit } from '@angular/core';
import { ParamMap, ActivatedRoute } from '@angular/router';
import { MapdataService } from '@services/mapdata.service';
import { switchMap } from 'rxjs/operators';

import { Measurement } from '@shared/interfaces/measurement';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-building-detail',
  templateUrl: './building-detail.component.html',
  styleUrls: ['./building-detail.component.scss']
})
export class BuildingDetailComponent implements OnInit {
  building$!: { [index: string]: any };
  bdata!: string;
  measureFields = [
    'lastEtdatetime',
    'updateEtdatetime',
    'minNz',
    'min',
    'max',
    'sum',
    'avg'
  ];
  displayFields = ['BLDG_Class'];

  constructor(
    private route: ActivatedRoute,
    private mapdataService: MapdataService
  ) {}

  isMeasure = (field: any) => typeof field === 'object';

  ngOnInit() {
    this.route.paramMap.subscribe((params: ParamMap) => {
      this.mapdataService.getBuilding(params.get('bldg')).subscribe(value => {
        for (const met in value.metrics) {
          if (value.metrics.hasOwnProperty(met)) {
            for (const measure in value.metrics[met]) {
              if (
                value.metrics[met].hasOwnProperty(measure) &&
                typeof value.metrics[met][measure] === 'number'
              ) {
                value.metrics[met][measure] = value.metrics[met][
                  measure
                ].toFixed(2);
              }
            }
          }
        }
        this.building$ = value;
      });
    });
  }
}
