import { Component, signal } from '@angular/core';
import { RouterModule, RouterOutlet, RouterLink } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';

@Component({
  selector: 'app-root',
  imports: [RouterModule, RouterOutlet, NavbarComponent],
  templateUrl: './app.html',
  standalone: true,
  styleUrls: ['./app.scss']
})
export class App {
  protected readonly title = signal('iot-smart-home');
}
