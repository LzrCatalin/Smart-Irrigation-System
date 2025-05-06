import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IntervalDialogComponent } from './interval-dialog.component';

describe('IntervalDialogComponent', () => {
  let component: IntervalDialogComponent;
  let fixture: ComponentFixture<IntervalDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [IntervalDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(IntervalDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
