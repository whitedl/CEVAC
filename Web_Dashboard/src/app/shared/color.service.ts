//Exists to centralize management of color in the app
//*primarily for the map and map keys at the moment*
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ColorService {
  colors = {
    ClemsonPalette: {
      ClemsonOrange: '#F66733',
      Regalia: '#522D80',
      Innovation: '#86898C'
    },
    ClemsonComplementary: {
      ClemsonOrange: '#F66733',
      Regalia: '#522D80',
      Complementary1: '#33e9f6',
      Complementary2: '#80692d'
    },
    ClemsonTetradic: {
      ClemsonOrange: '#F66733',
      Regalia: '#522D80',
      Tetradic1: '#57ebf6',
      Tetradic2: '#f6bf33'
    }
  }

  constructor() { }

  getComplementarySet() {
    return Object.values(this.colors.ClemsonComplementary);
  }

  getTetradicSet() {
    return Object.values(this.colors.ClemsonTetradic);
  }

  getColorSet(name: string) {
    if(name in this.colors)
      return Object.values(this.colors[name]);
    else return Object.values(this.colors.ClemsonPalette)
  }

  getActive() {
    return this.colors.ClemsonPalette.ClemsonOrange;
  }
  getPassive() {
    return this.colors.ClemsonPalette.Regalia;
  }
  getUnnamed() {
    return this.colors.ClemsonPalette.Innovation;
  }
}
