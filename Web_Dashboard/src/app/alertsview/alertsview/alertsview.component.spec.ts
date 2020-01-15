import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlertsviewComponent } from './alertsview.component';

describe('AlertsviewComponent', () => {
  let component: AlertsviewComponent;
  let fixture: ComponentFixture<AlertsviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlertsviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlertsviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
