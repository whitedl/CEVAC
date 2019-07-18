// Exists to centralize management of color in the app
// *primarily for the map and map keys at the moment*
import { Injectable } from '@angular/core';
import * as chroma from 'chroma-js';

interface Palette {
  [index: string]: string;
}
interface PaletteSet {
  [index: string]: Palette;
}

// Using a class for Scale makes life easier. You can't define a generic getter/setter for interfaces.
class Scale {
  domain: number[];
  get min() {
    return this.domain[0];
  }
  set min(n: number) {
    this.domain[0] = n;
  }
  get max() {
    return this.domain[this.domain.length - 1];
  }
  set max(n: number) {
    this.domain[this.domain.length - 1] = n;
  }
  constructor(domain: number[] = [0, 1000]) {
    this.domain = domain;
  }
}
interface ScaleSet {
  [index: string]: Scale;
}
interface BuildingRegistry {
  [index: string]: string;
}

@Injectable({
  providedIn: 'root'
})
export class ColorService {
  private colors: PaletteSet = {
    ClemsonPalette: {
      clemsonOrange: '#F66733',
      regalia: '#522D80',
      bowmansField: '#566127',
      centennialOak: '#562E19',
      hartwellMoon: '#D4C99E',
      howardsRock: '#685C53',
      blueRidge: '#3A4958',
      innovation: '#86898C'
    },
    ClemsonComplementary: {
      clemsonOrange: '#F66733',
      regalia: '#522D80',
      complementary1: '#33e9f6',
      complementary2: '#80692d'
    },
    ClemsonTetradic: {
      clemsonOrange: '#F66733',
      regalia: '#522D80',
      tetradic1: '#57ebf6',
      tetradic2: '#f6bf33'
    },
    Alerts: {
      alert: '#CC3300',
      warn: '#FFCC00'
    }
  };
  private scales: ScaleSet = {
    POWER: new Scale([0, 200, 400, 600, 800, 1000]),
    TEMP: new Scale([30, 60, 80, 100]),
    CO2: new Scale([0, 500, 800, 1000, 1200]),
    IAQ: new Scale([0, 500, 800, 1000, 1200]),
    CHW: new Scale([0, 10000]),
    HUMIDITY: new Scale([0, 70, 90, 100])
  };
  private crg: BuildingRegistry = {};
  private crgPalette = 'ClemsonPalette';

  constructor() {
    this.crg['undefined'] = this.getPassive();
  }

  // If name is not passed, assumes first ColorSet (ClemsonPalette).
  // If pos is passed, will return color at position in chosen set
  // If pos is not passed, will return first in set
  getColor = (
    name: string = Object.keys(this.colors)[0],
    pos: number = 0
  ): string => {
    if (!(name in this.colors)) {
      name = Object.keys(this.colors)[0];
    }
    const set = Object.values(this.colors[name]);
    return set[pos % set.length];
  };

  getColorScale = (category: string): chroma.Scale<chroma.Color> =>
    chroma
      .bezier(this.labDomain(this.crg[category]))
      .scale()
      .correctLightness();

  getScaledColor = (category: string, scale?: string, val?: number): string => {
    if (typeof val === 'undefined' || typeof scale === 'undefined') {
      return this.crg[category];
    }
    const domain = this.scales[scale].domain;
    const retScale = chroma
      .bezier(this.labDomain(this.crg[category]))
      .scale()
      // @ts-ignore
      // chroma.js typings don't include the nodata function
      .correctLightness();
    if (!val) {
      return retScale(0).name();
    } else if (domain.length !== 2) {
      return retScale
        .classes([...domain, domain[domain.length - 1]])(val)
        .name();
    } else {
      return retScale
        .domain(domain)(val)
        .name();
    }
  };

  registerCategory = (cat: string) => {
    if (!this.crg.hasOwnProperty(cat)) {
      this.crg[cat] = this.getColor(
        this.crgPalette,
        Object.keys(this.crg).length - 1
      );
    }
  };

  registerScale = (scale: string, domain: number[]) => {
    if (!this.scales.hasOwnProperty(scale)) {
      this.scales[scale] = new Scale(domain);
    }
  };

  getScale = (scaleType: string): number[] =>
    scaleType in this.scales ? this.scales[scaleType].domain : [-1, -1];

  setScale = (scaleType: string, domain: number[]) =>
    scaleType in this.scales ? (this.scales[scaleType].domain = domain) : null;

  // if scale is in Scales, return the lower bound
  scaleLowBound = (scaleType: string) =>
    scaleType in this.scales ? this.scales[scaleType].min : null;

  // if scale is in Scales, set the minimum. Returnset value on success and null on fail.
  setScaleLowBound = (scaleType: string, n: number) =>
    scaleType in this.scales ? (this.scales[scaleType].min = n) : null;

  // if scale is in Scales, return the upper bound
  scaleHighBound = (scaleType: string) =>
    scaleType in this.scales ? this.scales[scaleType].max : null;

  // if scale is in Scales, set the maximum. Returns set value on success and null on fail.
  setScaleHighBound = (scaleType: string, n: number) =>
    scaleType in this.scales ? (this.scales[scaleType].max = n) : null;

  getComplementary = (pos: number = 0) =>
    this.getColor('ClemsonComplementary', pos);

  getTetradic = (pos: number = 0) => this.getColor('ClemsonTetradic', pos);

  getActive = () => this.colors.ClemsonPalette.howardsRock;

  getPassive = () => this.colors.ClemsonPalette.blueRidge;

  getUnnamed = () => this.colors.ClemsonPalette.innovation;

  brighten = (color: string, n: number = 1) =>
    chroma(color)
      .brighten(n)
      .hex();
  darken = (color: string, n: number = 1) =>
    chroma(color)
      .darken(n)
      .hex();

  get alert() {
    return this.colors.Alerts.alert;
  }
  get warn() {
    return this.colors.Alerts.warn;
  }

  labDomain = (color: string): [string, string] => [
    this.labMax(color),
    this.labMin(color)
  ];
  private labMax = (color: string): string =>
    chroma(color)
      .set('lab.l', 90)
      .hex();
  private labMin = (color: string): string =>
    chroma(color)
      .set('lab.l', 10)
      .hex();
}
