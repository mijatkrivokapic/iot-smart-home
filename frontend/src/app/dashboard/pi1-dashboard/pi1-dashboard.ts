import { Component, OnInit } from '@angular/core';
import { SensorData, WebsocketMessage } from '../../models/sensor-data';
import { SensorService } from '../../services/sensor-service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AlarmService } from '../../services/alarm-service';

@Component({
  selector: 'app-pi1-dashboard',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatTableModule, FormsModule, MatInputModule, MatButtonModule],
  templateUrl: './pi1-dashboard.html',
  styleUrl: './pi1-dashboard.scss',
})
export class Pi1Dashboard implements OnInit {
  sensorData: { [key: string]: SensorData } = {};
  password: string = '';

  constructor(private sensorService: SensorService, private alarmService: AlarmService) {}

  ngOnInit(): void {
    this.sensorService.onPi1SensorUpdate().subscribe((data: WebsocketMessage) => {
      this.sensorData[data.payload.sensor] = data.payload;
    })
  }

  submitPassword(): void {
    this.alarmService.submitPassword(this.password).subscribe({
      next: (res) => {
        console.log('Password submit result', res);
        this.password = '';
      },
      error: (err) => {
        console.error('Password submit error', err);
      }
    });
  }
}
