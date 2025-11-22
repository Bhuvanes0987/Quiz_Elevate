import { ComponentFixture, TestBed } from '@angular/core/testing';
import { usercomponent } from './user.component'; // lowercase class

describe('usercomponent', () => {
  let component: usercomponent;
  let fixture: ComponentFixture<usercomponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [usercomponent] // only if standalone
      // If NOT standalone, replace with:
      // declarations: [usercomponent]
    }).compileComponents();

    fixture = TestBed.createComponent(usercomponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
