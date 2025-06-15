import { Routes } from '@angular/router';
import { AboutComponent } from './components/about/about';
import { SignupComponent } from './components/signup/signup';

export const routes: Routes = [
    { path: '', component: AboutComponent },
    { path: 'signup', component: SignupComponent },
    { path: '**', redirectTo: '' }
];
