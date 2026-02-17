import { Component, OnInit } from '@angular/core';
import { SensorService } from '../../services/sensor-service';
import { CommonModule } from '@angular/common';
import { WebsocketMessage } from '../../models/sensor-data';
import { RouterLinkWithHref } from '@angular/router';
import {MatCardModule} from '@angular/material/card';

@Component({
  selector: 'app-dashboard-component',
  imports: [CommonModule, RouterLinkWithHref, MatCardModule],
  templateUrl: './dashboard-component.html',
  styleUrl: './dashboard-component.scss',
})
export class DashboardComponent implements OnInit {
  sensors: WebsocketMessage[] = [];

  constructor(private sensorService: SensorService) {}


  ngOnInit(): void {
    this.sensorService.onSensorUpdate().subscribe((data) => {
      this.sensors.push(data);
    });
  }
}
