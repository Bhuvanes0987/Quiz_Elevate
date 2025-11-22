import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomFieldGroups } from './custom-field-groups';

describe('CustomFieldGroups', () => {
  let component: CustomFieldGroups;
  let fixture: ComponentFixture<CustomFieldGroups>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CustomFieldGroups]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CustomFieldGroups);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
