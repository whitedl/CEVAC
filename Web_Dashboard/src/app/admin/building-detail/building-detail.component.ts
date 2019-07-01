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
  private building$;

  constructor(
    private route: ActivatedRoute,
    private mapDataService: MapdataService
  ) {}

  ngOnInit() {
    this.building$ = this.route.paramMap.pipe(
      switchMap((params: ParamMap) => {
        console.log('hi');
        console.log(params.get('id'));
        return params.get('id');
      })
    );
  }
}
