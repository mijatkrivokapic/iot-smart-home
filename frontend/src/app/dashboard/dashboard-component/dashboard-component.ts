import { Component, OnInit } from '@angular/core';
import { SensorService } from '../../services/sensor-service';
import { CommonModule } from '@angular/common';
import { WebsocketMessage } from '../../models/sensor-data';
import { RouterLinkWithHref } from '@angular/router';
import {MatCardModule} from '@angular/material/card';
import {MatButton} from '@angular/material/button';
import {SystemStateService} from '../../services/system-state-service';

@Component({
  selector: 'app-dashboard-component',
  imports: [CommonModule, RouterLinkWithHref, MatCardModule, MatButton],
  templateUrl: './dashboard-component.html',
  styleUrl: './dashboard-component.scss',
  standalone: true
})
export class DashboardComponent implements OnInit {
  sensors: WebsocketMessage[] = [];
  state:any = null;

  constructor(private sensorService: SensorService,
              private systemStateService: SystemStateService) {}


  ngOnInit(): void {
    this.sensorService.onPi1SensorUpdate().subscribe((data) => {
      this.sensors.push(data);
    });

    this.systemStateService.onStateUpdate().subscribe((data) => {
      this.state = data;
      console.log(data);
    });

  }
}
