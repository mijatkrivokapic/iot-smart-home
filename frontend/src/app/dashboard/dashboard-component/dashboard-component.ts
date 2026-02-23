import { Component, OnInit } from '@angular/core';
import { SensorService } from '../../services/sensor-service';
import { CommonModule } from '@angular/common';
import { WebsocketMessage } from '../../models/sensor-data';
import { RouterLinkWithHref } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButton } from '@angular/material/button';
import { SystemStateService } from '../../services/system-state-service';
import { Pi1Dashboard } from '../pi1-dashboard/pi1-dashboard';
import { Pi2Dashboard } from '../pi2-dashboard/pi2-dashboard';
import { Pi3Dashboard } from '../pi3-dashboard/pi3-dashboard';

@Component({
  selector: 'app-dashboard-component',
  imports: [
    CommonModule,
    RouterLinkWithHref,
    MatCardModule,
    MatButton,
    Pi1Dashboard,
    Pi2Dashboard,
    Pi3Dashboard,
  ],
  templateUrl: './dashboard-component.html',
  styleUrl: './dashboard-component.scss',
  standalone: true,
})
export class DashboardComponent implements OnInit {
  sensors: WebsocketMessage[] = [];
  state: any = null;

  constructor(
    private sensorService: SensorService,
    private systemStateService: SystemStateService,
  ) {}

  ngOnInit(): void {
    this.sensorService.onPi1SensorUpdate().subscribe((data) => {
      this.sensors.push(data);
    });

    this.systemStateService.onStateUpdate().subscribe((data) => {
      this.state = data;
    });

    this.systemStateService.getCurrentState().subscribe((data) => {
      this.state = data;
    });
  }
}
