import { Injectable } from '@angular/core';
import { ColorService } from '@services/color.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

declare let L;
const geodata = require('src/assets/CU_Building_Footprints.json');

@Injectable({ providedIn: 'root' })
export class MapdataService {
  map;
  tracked;
  untracked;
  mapOptions = {
    minZoom: 15,
    maxZoom: 20
  };
  categories = {};
  functions = {};
  private dataUrl = 'http://wfic-cevac1/requests/stats.php';

  constructor(private colorService: ColorService, private http: HttpClient) {}

  getMap() {
    if (!this.map) {
      this.initMap();
    }
    return this.map;
  }

  initMap() {
    this.map = L.map('map', this.mapOptions).setView([34.6761, -82.8366], 16);
    const mapbox = this.getTileLayerMapboxLight().addTo(this.map);
    const controller = L.control
      .layers({ mapbox, openstreetmap: this.getTileLayerOpenMap() })
      .addTo(this.map);
    this.untracked = L.geoJSON(geodata, this.untrackedOptions).addTo(this.map);
    this.tracked = L.geoJSON(geodata, this.trackedOptions).addTo(this.map);
    controller.addOverlay(this.untracked, 'show untracked');
  }

  getTileLayerMapboxLight() {
    return L.tileLayer(
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
  }

  getTileLayerOpenMap() {
    return L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });
  }

  styleUntracked = feature => {
    const style = {};
    const funcCol = [];
    let catCol;
    style['fill'] = true;
    style['fillColor'] = this.colorService.getPassive();
    style['opacity'] = 1;
    style['fillOpacity'] = 0.8;
    if (feature.properties.Short_Name === ' ') {
      style['fillColor'] = this.colorService.getUnnamed();
    }
    if (feature.properties.Function) {
      for (const func of feature.properties.Function) {
        if (!(func in this.functions)) {
          this.functions[func] = this.colorService.getComplementary(
            Object.keys(this.functions).length
          );
        }
        funcCol.push(this.functions[func]);
      }
    } else {
      funcCol.push(this.colorService.getUnnamed());
    }
    if (feature.properties.BLDG_Class) {
      if (!(feature.properties.BLDG_Class in this.categories)) {
        this.categories[
          feature.properties.BLDG_Class
        ] = this.colorService.getComplementary(
          Object.keys(this.categories).length
        );
      }
      catCol = this.categories[feature.properties.BLDG_Class];
    } else {
      catCol = this.colorService.getUnnamed();
    }
    style['color'] = catCol;
    return style;
  };

  styleTracked = feature => {
    const style = {};
    const funcCol = [];
    let catCol;
    style['fill'] = true;
    style['fillColor'] = feature.properties.bData
      ? this.colorService.powerScale(feature.properties.bData.power_latest_sum)
      : this.colorService.getActive();
    style['weight'] = 4;
    style['opacity'] = 1;
    style['fillOpacity'] = 1;
    if (feature.properties.Function) {
      for (const func of feature.properties.Function) {
        if (!(func in this.functions)) {
          this.functions[func] = this.colorService.getComplementary(
            Object.keys(this.functions).length
          );
        }
        funcCol.push(this.functions[func]);
      }
    } else {
      funcCol.push(this.colorService.getUnnamed());
    }
    if (feature.properties.BLDG_Class) {
      if (!(feature.properties.BLDG_Class in this.categories)) {
        this.categories[
          feature.properties.BLDG_Class
        ] = this.colorService.getComplementary(
          Object.keys(this.categories).length
        );
      }
      catCol = this.categories[feature.properties.BLDG_Class];
    } else {
      catCol = this.colorService.getUnnamed();
    }
    style['color'] = catCol;
    return style;
  };

  highlightFeat(layer) {
    layer.setStyle({
      weight: 5,
      color: '#666',
      fillOpacity: 0.7
    });

    layer.bringToFront();
  }

  resetHighlight = e => {
    const layer = e.target;
    if (this.tracked.hasLayer(layer)) {
      this.tracked.resetStyle(layer);
    } else {
      this.untracked.resetStyle(layer);
    }
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

  zoomToFeat = e => {
    this.map.fitBounds(e.target.getBounds());
  };

  shortNameTooltip(layer) {
    if (layer.feature.properties.Short_Name !== ' ') {
      return layer.feature.properties.Short_Name;
    } else {
      return 'Short_Name not set';
    }
  }

  mouseOver = e => {
    const layer = e.target;
    this.highlightFeat(layer);
    if (!layer.isPopupOpen()) {
      layer.bindTooltip(this.shortNameTooltip).openTooltip();
    }
  };
  hideTooltip = e => {
    const layer = e.target;
    layer.unbindTooltip();
  };

  onEachFeat = (feature, layer) => {
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

  // tslint:disable-next-line: member-ordering
  untrackedOptions = {
    style: this.styleUntracked,
    onEachFeature: this.onEachFeat,
    filter(feature, layer) {
      return (
        !feature.properties.Status || feature.properties.Status !== 'Active'
      );
    }
  };

  // tslint:disable-next-line: member-ordering
  trackedOptions = {
    style: this.styleTracked,
    onEachFeature: this.onEachFeat,
    filter(feature, layer) {
      return feature.properties.Status === 'Active';
    }
  };
}
