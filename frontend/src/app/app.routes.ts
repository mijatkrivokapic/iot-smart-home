import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard-component/dashboard-component';
import { Pi1Dashboard } from './dashboard/pi1-dashboard/pi1-dashboard';

export const routes: Routes = [
    { path: "", component: DashboardComponent },
    { path: "pi1-dashboard", component: Pi1Dashboard },
];
