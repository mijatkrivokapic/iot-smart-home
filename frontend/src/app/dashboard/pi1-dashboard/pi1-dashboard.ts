import { Component, OnInit } from '@angular/core';
import { SensorData, WebsocketMessage } from '../../models/sensor-data';
import { SensorService } from '../../services/sensor-service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AlarmService } from '../../services/alarm-service';
import {environment} from '../../environment/environment';

@Component({
  selector: 'app-pi1-dashboard',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatTableModule, FormsModule, MatInputModule, MatButtonModule, MatIconModule],
  templateUrl: './pi1-dashboard.html',
  styleUrl: './pi1-dashboard.scss',
})
export class Pi1Dashboard implements OnInit {
  sensorData: { [key: string]: SensorData } = {};
  password: string = '';
  cameraUrl: string = `http://192.168.107.14${environment.pi1Id}:8080/?action=stream`;
  dlStatus:any = 0;

  constructor(private sensorService: SensorService, private alarmService: AlarmService) {}

  ngOnInit(): void {
    this.sensorService.onPi1SensorUpdate().subscribe((data: WebsocketMessage) => {
      if(data.payload.sensor === 'DL') {
        this.dlStatus = data.payload.value;
      }
      else{
        this.sensorData[data.payload.sensor] = data.payload;
      }

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
