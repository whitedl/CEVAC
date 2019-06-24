// Exists to centralize management of color in the app
// *primarily for the map and map keys at the moment*
import { Injectable } from '@angular/core';
import chroma from 'chroma-js';

interface Palette {
  [index: string]: string;
}
interface PaletteSet {
  [index: string]: Palette;
}
interface Scale {
  domain: [number, number];
  min: number;
  max: number;
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
  private Scales: ScaleSet = {
    Power: {
      domain: [0, 1000],
      get min() {
        return this.domain[0];
      },
      set min(n: number) {
        this.domain[0] = n;
      },
      get max() {
        return this.domain[1];
      },
      set max(n: number) {
        this.domain[1] = n;
      }
    },
    Temperature: {
      domain: [50, 100],
      get min() {
        return this.domain[0];
      },
      set min(n: number) {
        this.domain[0] = n;
      },
      get max() {
        return this.domain[1];
      },
      set max(n: number) {
        this.domain[1] = n;
      }
    },
    CO2: {
      domain: [0, 500],
      get min() {
        return this.domain[0];
      },
      set min(n: number) {
        this.domain[0] = n;
      },
      get max() {
        return this.domain[1];
      },
      set max(n: number) {
        this.domain[1] = n;
      }
    }
  };
  private crg: BuildingRegistry;
  private crgPalette = 'ClemsonComplementary';

  constructor() {}

  // If name is not passed, assumes first ColorSet (ClemsonPalette).
  // If pos is passed, will return color at position in chosen set
  // If pos is not passed, will return first in set
  getColor = (name: string = Object.keys(this.colors)[0], pos: number = 0) => {
    if (!(name in this.colors)) {
      name = Object.keys(this.colors)[0];
    }
    const set = Object.values(this.colors[name]);
    return set[pos % set.length];
  };

  getScaledColor = (category: string, scale: string, val: number) =>
    chroma
      .scale([this.crg[category], this.crg[category]])
      .domain(this.Scales[scale].domain)(val);

  registerCategory = (cat: string) => {
    if (!this.crg.hasOwnProperty(cat)) {
      this.crg[cat] = this.getColor(
        this.crgPalette,
        Object.keys(this.crg).length
      );
    }
  };

  // If n is not passed, will return requested scale
  // If scaleType is not passed, will assume first scale
  getScale = (n?: number, scaleType: string = Object.keys(this.Scales)[0]) => {
    if (!(scaleType in this.Scales)) {
      scaleType = Object.keys(this.Scales)[0];
    }
    const scale = this.Scales[scaleType];
    const c = chroma(this.getColor('ClemsonTetradic', 0));
    const low = c.set('lab.l', 0);
    const high = c.set('lab.l', 100);
    const s = chroma.scale([high, low]).domain(scale.domain);
    return typeof n !== 'undefined' ? s(n) : scale;
  };

  // if scale is in Scales, return the lower bound
  getScaleLower = (scaleType: string) =>
    scaleType in this.Scales ? this.Scales[scaleType].min : null;

  // if scale is in Scales, set the minimum. Returnset value on success and null on fail.
  setScaleLower = (n: number, scaleType: string) =>
    scaleType in this.Scales ? (this.Scales[scaleType].min = n) : null;

  // if scale is in Scales, return the upper bound
  getScaleHigher = (scaleType: string) =>
    scaleType in this.Scales ? this.Scales[scaleType].max : null;

  // if scale is in Scales, set the maximum. Returns set value on success and null on fail.
  setScaleHigher = (n: number, scaleType: string) =>
    scaleType in this.Scales ? (this.Scales[scaleType].max = n) : null;

  getComplementary = (pos: number = 0) =>
    this.getColor('ClemsonComplementary', pos);

  getTetradic = (pos: number = 0) => this.getColor('ClemsonTetradic', pos);

  getActive = () => this.colors.ClemsonPalette.howardsRock;

  getPassive = () => this.colors.ClemsonPalette.blueRidge;

  getUnnamed = () => this.colors.ClemsonPalette.innovation;

  get alert() {
    return this.colors.Alerts.alert;
  }
  get warn() {
    return this.colors.Alerts.warn;
  }
}
