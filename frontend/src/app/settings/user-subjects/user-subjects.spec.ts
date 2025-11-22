import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserSubjects } from './user-subjects';

describe('UserSubjects', () => {
  let component: UserSubjects;
  let fixture: ComponentFixture<UserSubjects>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserSubjects]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserSubjects);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
