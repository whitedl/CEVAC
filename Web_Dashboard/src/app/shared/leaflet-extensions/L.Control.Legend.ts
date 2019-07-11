import * as L from 'leaflet';
import { Measurement } from '@shared/interfaces/measurement';

export class Legend extends L.Control {
  options: L.ControlOptions = { position: 'bottomleft' };
  private scale: [number, number];
  private container: HTMLElement;
  private rangeHeader: HTMLElement;
  private scaleMax: HTMLElement;
  private scaleMin: HTMLElement;

  constructor(
    scale: [number, number],
    measurement: Measurement,
    options: L.ControlOptions
  ) {
    super(options);
    L.Util.setOptions(this, options);
    this.scale = scale;
    this.container = L.DomUtil.create('div', 'legend');
    const rangeContainer = L.DomUtil.create(
      'div',
      'legend-object',
      this.container
    );
    const scaleHeader = L.DomUtil.create('div', '', rangeContainer);
    this.rangeHeader = L.DomUtil.create('p', 'legend-header', scaleHeader);
    this.rangeHeader.textContent = measurement.name;
    this.scaleMax = L.DomUtil.create('div', '', scaleHeader);
    this.scaleMax.setAttribute('style', 'text-align: center;');
    this.scaleMax.textContent = this.scale[1].toString() + measurement.unit;
    this.scaleMin = L.DomUtil.create('div', '', rangeContainer);
    this.scaleMin.textContent = this.scale[0].toString() + measurement.unit;
  }
  onAdd(map: L.Map) {
    return this.container;
  }
  onRemove(map: L.Map) {}
  addCategory(cat: string, domain: [string, string]) {
    // Not using L.DomUtil.create's option to specify parent, as we need more control over placement
    const contain = L.DomUtil.create('div', 'legend-object');
    const title = L.DomUtil.create('p', 'legend-header', contain);
    title.innerText = cat;
    const grad = L.DomUtil.create('div', 'gradient-scale', contain);
    grad.setAttribute(
      'style',
      'background-image: linear-gradient(to top, ' +
        domain[0] +
        ', ' +
        domain[1] +
        ');'
    );
    this.container.insertAdjacentElement('beforeend', contain);
  }
  changeScale(scale: [number, number], measurement: Measurement) {
    this.rangeHeader.textContent = measurement.name;
    this.scaleMin.textContent = scale[0].toString() + measurement.unit;
    this.scaleMax.textContent = scale[1].toString() + measurement.unit;
  }
  update() {
    if (!this.container) {
      return this;
    }
  }
}
