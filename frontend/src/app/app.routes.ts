import { Routes } from '@angular/router'; 
import { LoginPage } from './pages/login/login';
import { SignupComponent } from './pages/sign-up/sign-up';
import { HomeComponent } from './pages/home/home';
import { InstructionsComponent } from './pages/instructions/instructions';
import { PaymentsComponent } from './pages/payments/payments';
import { ContactUsComponent } from './pages/contact-us/contact-us';
import { settingscomponent } from './pages/settings/settings';
import { UserComponent } from './settings/user/user.component';
import { UserSubjectsComponent } from './settings/user-subjects/user-subjects';
import { CustomFieldGroupsComponent } from './settings/custom-field-groups/custom-field-groups';
import { CustomFieldsComponent } from './settings/custom-fields/custom-fields';

export const routes: Routes = [
    { path: '', component: LoginPage }, 
    { path: 'signup', component: SignupComponent },
    { path: 'home', component: HomeComponent },
    { path: 'instructions', component: InstructionsComponent },
    { path: 'payments', component: PaymentsComponent },
    { path: 'contact-us', component: ContactUsComponent },
    { path: 'settings', component: settingscomponent },
    {
  path: "settings",
  component: settingscomponent,
  children: [
    { path: "user", component: UserComponent },
    { path: "user-subjects", component: UserSubjectsComponent },
    { path: "custom-field-groups", component: CustomFieldGroupsComponent },
    { path: "custom-fields", component: CustomFieldsComponent },

    // default route
    { path: "", redirectTo: "user", pathMatch: "full" }
  ]
}

];
