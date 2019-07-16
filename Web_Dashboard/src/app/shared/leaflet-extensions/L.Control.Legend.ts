import * as L from 'leaflet';
import * as chroma from 'chroma-js';
import { Measurement } from '@shared/interfaces/measurement';

export class Legend extends L.Control {
  options: L.ControlOptions = { position: 'bottomleft' };
  private scale: number[] = [0, 1000];
  private container: HTMLElement;
  private scaleElement: HTMLElement;
  private scaleHeader: HTMLElement;
  private scaleSteps: HTMLElement;
  private scales: [HTMLElement, chroma.Scale<chroma.Color>][] = [];

  constructor(
    scale: number[],
    measurement: Measurement,
    options: L.ControlOptions
  ) {
    super(options);
    L.Util.setOptions(this, options);
    this.scale = scale;
    this.container = L.DomUtil.create('div', 'legend');
    this.scaleElement = L.DomUtil.create(
      'div',
      'legend-object-left',
      this.container
    );
    this.scaleHeader = L.DomUtil.create(
      'p',
      'legend-header',
      this.scaleElement
    );
    this.scaleHeader.textContent = measurement.name;
    this.scaleSteps = L.DomUtil.create(
      'div',
      'flex-col flex-just-sb flex-fill',
      this.scaleElement
    );
    let i = scale.length;
    while (i--) {
      L.DomUtil.create('div', '', this.scaleSteps).textContent =
        scale[i].toString() + measurement.unit;
    }
  }
  onAdd(map: L.Map) {
    return this.container;
  }
  onRemove(map: L.Map) {}
  addCategory(cat: string, colorScale: chroma.Scale<chroma.Color>) {
    // Not using L.DomUtil.create's option to specify parent, as we need more control over placement
    const contain = L.DomUtil.create('div', 'legend-object');
    const title = L.DomUtil.create('p', 'legend-header', contain);
    title.innerText = cat;
    this.scales.push([L.DomUtil.create('div', 'scale', contain), colorScale]);
    this.scales[this.scales.length - 1][0].setAttribute(
      'style',
      'background-image: linear-gradient(to top, ' +
        colorScale(0) +
        ', ' +
        colorScale(1) +
        ');'
    );
    if (this.scale.length !== 2) {
      this.makeSteps(this.scales.length - 1);
    }
    this.container.insertAdjacentElement('beforeend', contain);
  }
  changeScale(scale: number[], measurement: Measurement) {
    this.scaleHeader.textContent = measurement.name;
    this.removeChildren(this.scaleSteps);
    let i = scale.length;
    while (i--) {
      L.DomUtil.create('div', '', this.scaleSteps).textContent =
        scale[i].toString() + measurement.unit;
    }
    if (this.scale.length !== scale.length) {
      this.scale = scale;
      i = this.scales.length;
      if (this.scale.length === 2) {
        while (i--) {
          this.removeChildren(this.scales[i][0]);
        }
      } else {
        while (i--) {
          this.makeSteps(i);
        }
      }
    }
  }
  removeChildren = (el: HTMLElement) => {
    while (el.firstChild) {
      el.removeChild(el.firstChild);
    }
  };
  makeSteps = (n: number) => {
    if (n < 0 || n >= this.scales.length) {
      return null;
    }
    const scale = this.scales[n];
    const colSet = scale[1].colors(this.scale.length);
    let i = colSet.length;
    while (i--) {
      L.DomUtil.create('div', 'flex-auto', scale[0]).setAttribute(
        'style',
        'background:' + colSet[i]
      );
    }
  };
  update() {
    if (!this.container) {
      return this;
    }
  }
}
