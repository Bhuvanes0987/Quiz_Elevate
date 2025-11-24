import { ComponentFixture, TestBed } from '@angular/core/testing';
import { UserComponent } from './user.component'; // lowercase class

describe('UserComponent', () => {
  let component: UserComponent;
  let fixture: ComponentFixture<UserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserComponent] // only if standalone
      // If NOT standalone, replace with:
      // declarations: [usercomponent]
    }).compileComponents();

    fixture = TestBed.createComponent(UserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
