import { Injectable } from '@angular/core';

declare let L;
var geodata = require('src/assets/CU_Building_Footprints.json');

@Injectable({ providedIn: 'root' })

export class MapdataService {

  constructor() { }
  
  map;
  tracked;
  untracked;
  mapOptions = {
	  minZoom: 15,
	  maxZoom: 20
  }
  untrackedColor = '#c51b8a';
  
  getMap () {
    if(!this.map) this.initMap();
    return this.map;
  }
  
  initMap () {
    this.map = L.map('map',this.mapOptions).setView([34.6761, -82.8366], 16);
    var mapbox = this.getTileLayerMapboxLight().addTo(this.map);
    var controller = L.control.layers(
      {mapbox,'openstreetmap':this.getTileLayerOpenMap()}
    ).addTo(this.map);
    this.untracked = L.geoJSON(geodata,this.untrackedOptions).addTo(this.map);
    this.tracked = L.geoJSON(geodata,this.trackedOptions).addTo(this.map);
    controller.addOverlay(this.untracked, 'show untracked');
  }
  
  getTileLayerMapboxLight() {
	  return L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={access_token}', {
			attribution: 'Map data &copy; <a href=https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
			id: 'mapbox.light',
			//Currently my personal token, should change to university token
			access_token: 'pk.eyJ1IjoienRrbGVpbiIsImEiOiJjanZ3aGdubWkwaWdiNGFwOXE0eW55ZG5jIn0.83eVqOeNMqaAywNFD0YqlQ'
	  });
  }
  
  getTileLayerOpenMap() {
	  return L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	  });
  }
  
  isActive(feature) {
	switch(feature.properties.Short_Name) {
			case 'ASC': //ASC
				return true;
			case 'Watt': //Watt
				return true;
			default:
				return false;
		}
  }
  
  styleUntracked = (feature) => {
    var style = {};
    if(this.isActive(feature)) {
      style['opacity'] = 0;
      style['fillOpacity'] = 0;
    } else {
      style['color'] = this.untrackedColor;
    }
    if(feature.properties.Short_Name == " ") style['color'] = '#666';
    return style;
  }
  styleTracked = (feature) => {
    var style = {};
    if(this.isActive(feature)){
      style['opacity'] = 0.8;
      style['fillOpacity'] = 0.8;
    } else {
      style['opacity'] = 0;
      style['fillOpacity'] = 0;
    }
    return style;
  }
  
  highlightFeat(e) {
    var layer = e.target;
    layer.setStyle({
      weight: 5,
      color: '#666',
      fillOpacity: 0.7
    });
    
    layer.bringToFront;
  }
  resetHighlight = (e) => {
    if(this.tracked.hasLayer(e.target)) this.tracked.resetStyle(e.target);
    else this.untracked.resetStyle(e.target);
  }
  zoomToFeat = (e) => {
    this.map.fitBounds(e.target.getBounds());
  }
  
  onEachFeat = (feature, layer) => {
    var opt = {
      mouseover: this.highlightFeat,
      click: this.zoomToFeat,
      mouseout: this.resetHighlight
    };
    layer.on(opt);
    layer.bindTooltip(function(layer){
      if(layer.feature.properties.Short_Name != " ")
      return layer.feature.properties.Short_Name;
      else return "Short_Name not set";
    });
  }
  
  untrackedOptions = {
    style: this.styleUntracked,
    onEachFeature: this.onEachFeat
  }
  
  trackedOptions = {
    style: this.styleTracked,
    onEachFeature: this.onEachFeat
  }
}
