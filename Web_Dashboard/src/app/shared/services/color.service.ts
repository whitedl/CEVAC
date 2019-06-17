// Exists to centralize management of color in the app
// *primarily for the map and map keys at the moment*
import { Injectable } from '@angular/core';
import chroma from 'chroma-js';

@Injectable({
  providedIn: 'root'
})
export class ColorService {
  private colors = {
    ColorSets: {
      ClemsonPalette: {
        clemsonOrange: '#F66733',
        regalia: '#522D80',
        hartwellMoon: '#D4C99E',
        howardsRock: '#685C53',
        blueRidge: '#3A4958',
        innovation: '#86898C'
      },
      ClemsonComplementary: {
        ClemsonOrange: '#F66733',
        regalia: '#522D80',
        complementary1: '#33e9f6',
        complementary2: '#80692d'
      },
      ClemsonTetradic: {
        ClemsonOrange: '#F66733',
        regalia: '#522D80',
        tetradic1: '#57ebf6',
        tetradic2: '#f6bf33'
      },
      Alerts: {
        alert: '#CC3300',
        warn: '#FFCC00'
      }
    },
    Scales: {
      Power: {
        min: 0,
        max: 1000,
        get scale() {
          return chroma.scale('Reds').domain([this.min, this.max]);
        }
      },
      Temperature: {
        min: 50,
        max: 100,
        get scale() {
          return chroma.scale('Blues').domain([this.min, this.max]);
        }
      },
      CO2: {
        min: 0,
        max: 500,
        get scale() {
          return chroma.scale('Greens').domain([this.min, this.max]);
        }
      }
    }
  };

  constructor() {}

  // If n is not passed, will return requested scale
  // If scaleType is not passed, will assume first scale
  getScale = (
    n?: number,
    scaleType: string = Object.keys(this.colors.Scales)[0]
  ) => {
    if (!(scaleType in this.colors.Scales)) {
      scaleType = Object.keys(this.colors.Scales)[0];
    }
    const scale = this.colors.Scales[scaleType].scale;
    return typeof n !== 'undefined' ? scale(n) : scale;
  };

  // if scale is in Scales, return the lower bound
  getScaleLower = (scaleType: string) =>
    scaleType in this.colors.Scales ? this.colors.Scales[scaleType].min : null;

  // if scale is in Scales, set the minimum. Returnset value on success and null on fail.
  setScaleLower = (n: number, scaleType: string) =>
    scaleType in this.colors.Scales
      ? (this.colors.Scales[scaleType].min = n)
      : null;

  // if scale is in Scales, return the upper bound
  getScaleHigher = (scaleType: string) =>
    scaleType in this.colors.Scales ? this.colors.Scales['notthere'].max : null;

  // if scale is in Scales, set the maximum. Returns set value on success and null on fail.
  setScaleHigher = (n: number, scaleType: string) =>
    scaleType in this.colors.Scales
      ? (this.colors.Scales[scaleType].max = n)
      : null;

  // If name is not passed, assumes first ColorSet (ClemsonPalette).
  // If pos is passed, will return color at position in chosen set
  // If pos is not passed, will return requested set
  getColor = (name = Object.keys(this.colors.ColorSets)[0], pos?: number) => {
    if (!(name in this.colors.ColorSets)) {
      name = Object.keys(this.colors.ColorSets)[0];
    }
    const set = Object.values(this.colors.ColorSets[name]);
    return typeof pos !== 'undefined' ? set[pos % set.length] : set;
  };

  getComplementary = (pos?: number) =>
    this.getColor('ClemsonComplementary', pos);

  getTetradic = (pos?: number) => this.getColor('ClemsonTetradic', pos);

  getActive = () => this.colors.ColorSets.ClemsonPalette.howardsRock;

  getPassive = () => this.colors.ColorSets.ClemsonPalette.blueRidge;

  getUnnamed = () => this.colors.ColorSets.ClemsonPalette.innovation;

  get alert() {
    return this.colors.ColorSets.Alerts.alert;
  }
  get warn() {
    return this.colors.ColorSets.Alerts.warn;
  }
}
