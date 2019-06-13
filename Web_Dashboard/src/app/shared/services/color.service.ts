// Exists to centralize management of color in the app
// *primarily for the map and map keys at the moment*
import { Injectable } from '@angular/core';
import chroma from 'chroma-js';

@Injectable({
  providedIn: 'root'
})
export class ColorService {
  private colors = {
    ClemsonPalette: {
      ClemsonOrange: '#F66733',
      Regalia: '#522D80',
      HartwellMoon: '#D4C99E',
      HowardsRock: '#685C53',
      BlueRidge: '#3A4958',
      Innovation: '#86898C'
    },
    ClemsonComplementary: {
      // ClemsonOrange: '#F66733',
      Regalia: '#522D80',
      Complementary1: '#33e9f6',
      Complementary2: '#80692d'
    },
    ClemsonTetradic: {
      // ClemsonOrange: '#F66733',
      Regalia: '#522D80',
      Tetradic1: '#57ebf6',
      Tetradic2: '#f6bf33'
    }
  };

  constructor() {}

  // If name is not passed, assumes first color (ClemsonPalette).
  // If pos is passed, will return color at position in chosen set
  // If pos is not passed, will return requested set
  getColor(name = Object.keys(this.colors)[0], pos?: number) {
    const set = Object.values(this.colors[name]);
    return typeof pos !== 'undefined' ? set[pos % set.length] : set;
  }

  getComplementary(pos?: number) {
    return this.getColor('ClemsonComplementary', pos);
  }

  getTetradic(pos?: number) {
    return this.getColor('ClemsonTetradic', pos);
  }

  getActive() {
    return this.colors.ClemsonPalette.ClemsonOrange;
  }
  getPassive() {
    return this.colors.ClemsonPalette.BlueRidge;
  }
  getUnnamed() {
    return this.colors.ClemsonPalette.Innovation;
  }
}
