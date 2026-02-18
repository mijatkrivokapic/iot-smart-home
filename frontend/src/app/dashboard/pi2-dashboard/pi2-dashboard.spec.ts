import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pi2Dashboard } from './pi2-dashboard';

describe('Pi2Dashboard', () => {
  let component: Pi2Dashboard;
  let fixture: ComponentFixture<Pi2Dashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Pi2Dashboard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Pi2Dashboard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
