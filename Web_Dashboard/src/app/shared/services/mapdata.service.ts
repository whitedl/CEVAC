import { Injectable } from '@angular/core';
import { ColorService } from '@services/color.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

declare const L: any;
const geodata = require('src/assets/CU_Building_Footprints.json');
interface DataSet {
  name: string;
  propertyName: string;
}

@Injectable({ providedIn: 'root' })
export class MapdataService {
  // be sure the names match with the values in color service, otherwise you'll get the default scale
  dataSets: DataSet[] = [
    { name: 'Power', propertyName: 'power_latest_sum' },
    { name: 'Temperature', propertyName: 'temp_latest_avg' },
    { name: 'CO2', propertyName: 'co2_latest_avg' }
  ];
  dataSet: DataSet = this.dataSets[0];

  private dataUrl = 'http://wfic-cevac1/requests/stats.php';
  private sasBaseURL =
    'https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=';
  private map;
  private tracked;
  private untracked;
  private mapOptions = {
    minZoom: 15,
    maxZoom: 20
  };
  private categories = {};
  private functions = {};

  constructor(private colorService: ColorService, private http: HttpClient) {}

  getMap = () => (!this.map ? this.initMap() : this.map);

  setDataSet = () => {
    this.tracked.setStyle(this.styleTracked);
  };

  focusBldg = (bldg: string) => {
    let layers = this.tracked.getLayers();
    for (const layer of layers) {
      if (layer.feature.properties.Short_Name === bldg) {
        this.map.fitBounds(layer.getBounds());
        return;
      }
    }
    layers = this.untracked.getLayers();
    for (const layer of layers) {
      if (layer.feature.properties.Short_Name === bldg) {
        this.map.fitBounds(layer.getBounds());
      }
    }
  };

  private initMap = () => {
    for (const feature of geodata.features) {
      if (feature.properties.Function) {
        for (const func of feature.properties.Function) {
          if (!(func in this.functions)) {
            this.functions[func] = this.colorService.getComplementary(
              Object.keys(this.functions).length
            );
          }
        }
      }
      if (feature.properties.BLDG_Class) {
        if (!(feature.properties.BLDG_Class in this.categories)) {
          this.categories[
            feature.properties.BLDG_Class
          ] = this.colorService.getComplementary(
            Object.keys(this.categories).length
          );
        }
      }
    }
    this.map = L.map('map', this.mapOptions).setView([34.6761, -82.8366], 16);
    const mapbox = this.getTileLayerMapboxLight().addTo(this.map);
    const controller = L.control
      .layers({ mapbox, openstreetmap: this.getTileLayerOpenMap() })
      .addTo(this.map);
    this.untracked = L.geoJSON(geodata, this.untrackedOptions).addTo(this.map);
    this.tracked = L.geoJSON(geodata, this.trackedOptions).addTo(this.map);
    controller.addOverlay(this.untracked, 'show untracked');
    return this.map;
  };

  private getTileLayerMapboxLight = () =>
    L.tileLayer(
      'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={access_token}',
      {
        attribution:
          // tslint:disable-next-line: max-line-length
          'Map data &copy; <a href=https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.light',
        // Currently my personal token, should change to university token
        access_token:
          'pk.eyJ1IjoienRrbGVpbiIsImEiOiJjanZ3aGdubWkwaWdiNGFwOXE0eW55ZG5jIn0.83eVqOeNMqaAywNFD0YqlQ'
      }
    );

  private getTileLayerOpenMap = () =>
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });

  private styleUntracked = feature => {
    const style = {};
    const funcCol = [];
    let catCol;
    style['fill'] = true;
    style['fillColor'] =
      feature.properties.BLDG_NAME !== ' '
        ? this.colorService.getPassive()
        : this.colorService.getUnnamed();
    style['opacity'] = 1;
    style['fillOpacity'] = 0.8;
    if (feature.properties.Function) {
      for (const func of feature.properties.Function) {
        funcCol.push(this.functions[func]);
      }
    } else {
      funcCol.push(this.colorService.getUnnamed());
    }
    if (feature.properties.BLDG_Class) {
      catCol = this.categories[feature.properties.BLDG_Class];
    } else {
      catCol = this.colorService.getUnnamed();
    }
    style['color'] = catCol;
    return style;
  };

  private styleTracked = feature => {
    const style = {};
    const funcCol: string[] = [];
    let catCol: string;
    style['fill'] = true;
    style['weight'] = 2;
    style['opacity'] = 1;
    style['fillOpacity'] = 1;
    if (feature.properties.Function) {
      for (const func of feature.properties.Function) {
        funcCol.push(this.functions[func]);
      }
    } else {
      funcCol.push(this.colorService.getUnnamed());
    }
    if (feature.properties.BLDG_Class) {
      catCol = this.categories[feature.properties.BLDG_Class];
    } else {
      catCol = this.colorService.getUnnamed();
    }
    style['color'] = catCol;
    style['fillColor'] =
      feature.properties.bData &&
      feature.properties.bData[this.dataSet.propertyName]
        ? this.colorService.getScale(
            feature.properties.bData[this.dataSet.propertyName],
            this.dataSet.name
          )
        : this.colorService.getActive();
    return style;
  };

  private highlightFeat = layer => {
    layer.setStyle({
      weight: 5,
      color: '#666',
      fillOpacity: 0.7
    });
    layer.bringToFront();
  };

  private resetHighlight = e => {
    const layer = e.target;
    if (this.tracked.hasLayer(layer)) {
      this.tracked.resetStyle(layer);
    } else {
      this.untracked.resetStyle(layer);
    }
  };

  private zoomToFeat = e => {
    this.map.fitBounds(e.target.getBounds());
  };

  private mouseOver = e => {
    const layer = e.target;
    this.highlightFeat(layer);
    if (!layer.isPopupOpen()) {
      layer.bindTooltip(this.longNameTooltip).openTooltip();
    }
  };

  private hideTooltip = e => {
    const layer = e.target;
    layer.unbindTooltip();
  };

  private onEachFeat = (feature, layer) => {
    const opt = {
      mouseover: this.mouseOver,
      click: this.hideTooltip,
      dblclick: this.zoomToFeat,
      mouseout: this.resetHighlight
    };
    layer.on(opt);
    this.http
      .get(this.dataUrl + '?building=' + layer.feature.properties.Short_Name)
      .subscribe(bData => {
        if (bData) {
          layer.feature.properties['bData'] = bData;
          this.tracked.resetStyle(layer);
        }
        layer.bindPopup(
          '<pre>' +
            JSON.stringify(layer.feature.properties, null, ' ').replace(
              /[\{\}"]/g,
              ''
            ) +
            '</pre>'
        );
      });
  };

  private longNameTooltip = layer =>
    layer.feature.properties.BLDG_NAME !== ' '
      ? layer.feature.properties.BLDG_NAME
      : 'Long_Name not set';

  private shortNameTooltip = layer =>
    layer.feature.properties.Short_Name !== ' '
      ? layer.feature.properties.Short_Name
      : 'Short_Name not set';

  private get untrackedOptions() {
    return {
      style: this.styleUntracked,
      onEachFeature: this.onEachFeat,
      filter(feature, layer) {
        return (
          !feature.properties.Status || feature.properties.Status !== 'Active'
        );
      }
    };
  }

  private get trackedOptions() {
    return {
      style: this.styleTracked,
      onEachFeature: this.onEachFeat,
      filter(feature, layer) {
        return feature.properties.Status === 'Active';
      }
    };
  }
}
