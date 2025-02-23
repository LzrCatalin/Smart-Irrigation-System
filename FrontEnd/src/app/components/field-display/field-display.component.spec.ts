import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FieldDisplayComponent } from './field-display.component';

describe('FieldDisplayComponent', () => {
  let component: FieldDisplayComponent;
  let fixture: ComponentFixture<FieldDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FieldDisplayComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FieldDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
