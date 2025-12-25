import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomFieldGroupsComponent } from './custom-field-groups.component';

describe('CustomFieldGroups', () => {
  let component: CustomFieldGroupsComponent;
  let fixture: ComponentFixture<CustomFieldGroupsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CustomFieldGroupsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CustomFieldGroupsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
