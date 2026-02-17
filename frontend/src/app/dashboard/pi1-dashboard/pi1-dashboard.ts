import { Component, OnInit } from '@angular/core';
import { SensorData, WebsocketMessage } from '../../models/sensor-data';
import { SensorService } from '../../services/sensor-service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-pi1-dashboard',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatTableModule],
  templateUrl: './pi1-dashboard.html',
  styleUrl: './pi1-dashboard.scss',
})
export class Pi1Dashboard implements OnInit {
  sensorData: { [key: string]: SensorData } = {};

  constructor(private sensorService: SensorService) {}

  ngOnInit(): void {
    this.sensorService.onSensorUpdate().subscribe((data: WebsocketMessage) => {
      this.sensorData[data.payload.sensor] = data.payload;
    })
  }
}
