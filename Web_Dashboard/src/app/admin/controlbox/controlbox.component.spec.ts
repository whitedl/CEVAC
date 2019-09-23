import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ControlboxComponent } from './controlbox.component';

describe('ControlboxComponent', () => {
  let component: ControlboxComponent;
  let fixture: ComponentFixture<ControlboxComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ControlboxComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ControlboxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
