import { Injectable } from '@angular/core';
import { ColorService } from '@services/color.service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import * as L from 'leaflet';

import { Legend } from '@shared/leaflet-extensions/L.Control.Legend';

import { Measurement } from '@shared/interfaces/measurement';
import { BuildingData } from '@shared/interfaces/buildingdata';

const geodata = require('src/assets/CU_Building_Footprints.json');

@Injectable({ providedIn: 'root' })
export class MapdataService {
  // be sure the names match with the values in color service, otherwise you'll get the default scale
  dataSets: Measurement[] = [
    { name: 'Power', propertyName: 'power_latest_sum', unit: 'kW' },
    { name: 'Temperature', propertyName: 'temp_latest_avg', unit: 'F' },
    { name: 'CO2', propertyName: 'co2_latest_avg', unit: 'ppm' }
  ];
  dataSet: Measurement = this.dataSets[0];

  private dataUrl = 'http://wfic-cevac1/requests/stats.php';
  private sasBaseURL =
    'https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=';
  private map!: L.Map;
  private tracked!: L.GeoJSON;
  private untracked!: L.GeoJSON;
  private mapOptions: L.MapOptions = {
    minZoom: 15,
    maxZoom: 18
  };
  private categories: Set<string> = new Set();
  private legend!: Legend;

  constructor(
    private colorService: ColorService,
    private http: HttpClient,
    private router: Router
  ) {}

  getMap = () => (!this.map ? this.initMap() : this.map);

  getBuilding = (bName: string | null) => {
    let building!: { [index: string]: any };
    this.map.eachLayer(layer => {
      const l = layer as L.Polygon;
      if (!building && l.feature && l.feature.properties.Short_Name === bName) {
        building = l.feature.properties;
        return building;
      }
    });
    if (!building || bName === ' ' || bName === null) {
      building = { Short_Name: 'Building not found' };
    }
    return building;
  };

  setDataSet = () => {
    this.tracked.setStyle(this.style);
    this.legend.changeScale(
      this.colorService.getScale(this.dataSet.name),
      this.dataSet
    );
  };

  focusBldg = (bldg: string) => {
    let layers: L.Polygon[] = this.tracked.getLayers() as L.Polygon[];
    for (const layer of layers) {
      if (layer.feature && layer.feature.properties.Short_Name === bldg) {
        this.map.fitBounds(layer.getBounds());
        this.router.navigate(['map', bldg]);
        return;
      }
    }
    layers = this.untracked.getLayers() as L.Polygon[];
    for (const layer of layers) {
      if (layer.feature && layer.feature.properties.Short_Name === bldg) {
        this.map.fitBounds(layer.getBounds());
        this.router.navigate(['map', bldg]);
      }
    }
  };

  private initMap = () => {
    for (const feature of geodata.features) {
      const bclass = feature.properties.BLDG_Class;
      if (!this.categories.has(bclass)) {
        this.categories.add(bclass);
        this.colorService.registerCategory(bclass);
      }
    }
    this.map = L.map('map', this.mapOptions).setView([34.678, -82.838], 17);
    const mapbox = this.getTileLayerMapboxLight().addTo(this.map);
    const controller = L.control
      .layers({ mapbox, openstreetmap: this.getTileLayerOpenMap() })
      .addTo(this.map);
    this.untracked = L.geoJSON(geodata, this.untrackedOptions).addTo(this.map);
    this.tracked = L.geoJSON(geodata, this.trackedOptions).addTo(this.map);
    controller.addOverlay(this.untracked, 'show untracked');
    this.legend = new Legend(
      this.colorService.getScale(this.dataSet.name),
      this.dataSet,
      { position: 'bottomleft' }
    );
    for (const cat of this.categories) {
      if (typeof cat !== 'undefined') {
        this.legend.addCategory(
          cat,
          this.colorService.labDomain(this.colorService.getScaledColor(cat))
        );
      }
    }
    this.legend.addTo(this.map);
    this.getBuilding('WATT');
    return this.map;
  };

  private getTileLayerMapboxLight = () =>
    L.tileLayer(
      'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={access_token}',
      {
        attribution:
          // tslint:disable-next-line: max-line-length
          '<a href="http://mapbox.com/about/maps" class="mapbox-wordmark" target="_blank"></a>© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>',
        id: 'mapbox.light',
        // Currently my personal token, should change to university token
        access_token:
          'pk.eyJ1IjoienRrbGVpbiIsImEiOiJjanZ3aGdubWkwaWdiNGFwOXE0eW55ZG5jIn0.83eVqOeNMqaAywNFD0YqlQ'
      } as L.TileLayerOptions
    );

  private getTileLayerOpenMap = () =>
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        'Map data and Imagery <a href="https://www.openstreetmap.org/copyright">&#169; OpenStreetMap</a>'
    });

  private style = (feature?: GeoJSON.Feature<GeoJSON.GeometryObject, any>) => {
    const style: L.PathOptions = {};
    if (feature) {
      const bclass: string = feature.properties.BLDG_Class;
      style.fill = true;
      style.weight = 1;
      style.opacity = 1;
      style.fillOpacity = 1;
      style.color = this.colorService.getScaledColor(bclass);
      style.fillColor =
        feature.properties &&
        feature.properties.bData &&
        feature.properties.bData[this.dataSet.propertyName]
          ? this.colorService.getScaledColor(
              bclass,
              this.dataSet.name,
              feature.properties.bData[this.dataSet.propertyName]
            )
          : this.colorService.getScaledColor(bclass, this.dataSet.name, 0);
    }
    return style;
  };

  private highlightFeat = (layer: L.Polygon) => {
    layer.setStyle({
      weight: 5,
      color: this.colorService.brighten(layer.options.color as string),
      fillColor: this.colorService.brighten(layer.options.fillColor as string)
    });
    layer.bringToFront();
  };

  private resetHighlight = (e: L.LeafletEvent) => {
    const layer = e.target;
    if (this.tracked.hasLayer(layer)) {
      this.tracked.resetStyle(layer);
    } else {
      this.untracked.resetStyle(layer);
    }
  };

  private zoomToFeat = (e: L.LeafletEvent) => {
    this.map.fitBounds(e.target.getBounds());
  };

  private mouseOver = (e: L.LeafletEvent) => {
    const layer = e.target;
    this.highlightFeat(layer);
    if (!layer.isPopupOpen()) {
      layer.bindTooltip(this.longNameTooltip).openTooltip();
    }
  };

  private hideTooltip = (e: L.LeafletEvent) => {
    const layer = e.target;
    layer.unbindTooltip();
  };

  private selectBuilding = (e: L.LeafletEvent) => {
    const layer = e.target;
    const bldg = layer.feature.properties.Short_Name;
    this.router.navigate(['map', bldg]);
  };

  private onClick = (e: L.LeafletEvent) => {
    this.hideTooltip(e);
    this.selectBuilding(e);
  };

  private onEachFeat = (
    feature: GeoJSON.Feature<GeoJSON.GeometryObject, any>,
    layer: L.Polygon
  ) => {
    const opt = {
      mouseover: this.mouseOver,
      click: this.onClick,
      mouseout: this.resetHighlight
    };
    layer.on(opt);
    if (feature.properties.Status === 'Active') {
      this.http
        .get(this.dataUrl + '?building=' + feature.properties.Short_Name)
        .subscribe((bData: BuildingData) => {
          if (bData) {
            bData.report_link = this.sasBaseURL + bData.report_link;
            feature.properties.bData = bData;
            this.tracked.resetStyle(layer);
          }
          layer.bindPopup(
            '<pre>' +
              JSON.stringify(feature.properties, null, ' ').replace(
                /[\{\}"]/g,
                ''
              ) +
              '</pre>'
          );
        });
    } else {
      layer.bindPopup(
        '<pre>' +
          JSON.stringify(feature.properties, null, ' ').replace(
            /[\{\}"]/g,
            ''
          ) +
          '</pre>'
      );
    }
  };

  private longNameTooltip = (layer: L.Polygon) =>
    layer.feature && layer.feature.properties.BLDG_NAME !== ' '
      ? layer.feature.properties.BLDG_NAME
      : 'Long_Name not set';

  private shortNameTooltip = (layer: L.Polygon) =>
    layer.feature && layer.feature.properties.Short_Name !== ' '
      ? layer.feature.properties.Short_Name
      : 'Short_Name not set';

  private get untrackedOptions(): L.GeoJSONOptions {
    return {
      style: this.style,
      onEachFeature: this.onEachFeat,
      filter(feature: GeoJSON.Feature<GeoJSON.Geometry, any>) {
        return feature.properties && feature.properties.Status !== 'Active';
      }
    };
  }

  private get trackedOptions(): L.GeoJSONOptions {
    return {
      style: this.style,
      onEachFeature: this.onEachFeat,
      filter(feature: GeoJSON.Feature<GeoJSON.Geometry, any>) {
        return feature.properties && feature.properties.Status === 'Active';
      }
    };
  }
}
