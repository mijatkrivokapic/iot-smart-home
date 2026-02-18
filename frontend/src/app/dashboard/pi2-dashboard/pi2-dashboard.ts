import {Component, OnInit} from '@angular/core';
import {SensorData, WebsocketMessage} from '../../models/sensor-data';
import {SensorService} from '../../services/sensor-service';
import {CommonModule} from '@angular/common';
import {MatCardModule} from '@angular/material/card';
import {MatTableModule} from '@angular/material/table';

@Component({
  selector: 'app-pi2-dashboard',
  imports: [CommonModule, MatCardModule, MatTableModule],
  templateUrl: './pi2-dashboard.html',
  styleUrl: './pi2-dashboard.scss',
  standalone: true
})
export class Pi2Dashboard implements OnInit {
  sensorData: { [key: string]: SensorData } = {};

  constructor(private sensorService: SensorService) {}

  ngOnInit(): void {
    this.sensorService.onPi2SensorUpdate().subscribe((data: WebsocketMessage) => {
      this.sensorData[data.payload.sensor] = data.payload;
    })
  }
}
