import { Routes } from '@angular/router'; 
import { LoginPage } from './pages/login/login';
import { SignupComponent } from './pages/sign-up/sign-up';
import { HomeComponent } from './pages/home/home';

export const routes: Routes = [
    { path: '', component: LoginPage }, 
    { path: 'signup', component: SignupComponent },
    { path: 'home', component: HomeComponent },
    
    // { path: '**', redirectTo: '' }
];
