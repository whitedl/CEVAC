// Exists to centralize management of color in the app
// *primarily for the map and map keys at the moment*
import { Injectable } from '@angular/core';
import chroma from 'chroma-js';
import { fromStringWithSourceMap } from 'source-list-map';

@Injectable({
  providedIn: 'root'
})
export class ColorService {
  private colors = {
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
  private Scales = {
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

  private regScales: Map<string, any>;

  constructor() {
    this.regScales = new Map<string, any>();
  }

  getRegisteredScale = (
    color: string,
    n?: number,
    scaleType: string = Object.keys(this.Scales)[0]
  ) => {
    if (!this.regScales.has(color)) {
      const c = chroma(color);
      const low = chroma.set('lch.l', 0);
      const high = chroma.set('lch.l', 100);
      this.regScales.set(color, chroma.scale([low, high]));
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

  // If name is not passed, assumes first ColorSet (ClemsonPalette).
  // If pos is passed, will return color at position in chosen set
  // If pos is not passed, will return requested set
  getColor = (name = Object.keys(this.colors)[0], pos?: number) => {
    if (!(name in this.colors)) {
      name = Object.keys(this.colors)[0];
    }
    const set = Object.values(this.colors[name]);
    return typeof pos !== 'undefined' ? set[pos % set.length] : set;
  };

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
