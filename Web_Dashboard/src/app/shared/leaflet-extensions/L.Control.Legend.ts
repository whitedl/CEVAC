import * as L from 'leaflet';

export class Legend extends L.Control {
  options: L.ControlOptions = { position: 'bottomleft' };
  private scale: [number, number];
  private container: HTMLElement;
  private rangeHeader: HTMLElement;
  private scaleMax: HTMLElement;
  private scaleMin: HTMLElement;

  constructor(
    scale: [number, number],
    rangeTitle: string,
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
    this.rangeHeader.textContent = rangeTitle;
    this.scaleMax = L.DomUtil.create('div', '', scaleHeader);
    this.scaleMax.setAttribute('style', 'text-align: center;');
    this.scaleMax.textContent = this.scale[1].toString();
    this.scaleMin = L.DomUtil.create('div', '', rangeContainer);
    this.scaleMin.textContent = this.scale[0].toString();
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
  changeScale(scale: [number, number], rangeHead: string) {
    this.rangeHeader.textContent = rangeHead;
    this.scaleMin.textContent = scale[0].toString();
    this.scaleMax.textContent = scale[1].toString();
  }
  update() {
    if (!this.container) {
      return this;
    }
  }
}
