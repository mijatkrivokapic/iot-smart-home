import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { SensorService } from '../../services/sensor-service';
import { RgbService } from '../../services/rgb-service';
import { SensorData, WebsocketMessage } from '../../models/sensor-data';

@Component({
  selector: 'app-pi3-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    FormsModule,
  ],
  templateUrl: './pi3-dashboard.html',
  styleUrls: ['./pi3-dashboard.scss'],
})
export class Pi3Dashboard implements OnInit {
  sensorData: { [key: string]: SensorData } = {};
  r: number = 0;
  g: number = 0;
  b: number = 0;

  color: string = '';

  constructor(
    private sensorService: SensorService,
    private rgbService: RgbService,
  ) {}

  ngOnInit(): void {
    this.sensorService.onPi3SensorUpdate().subscribe((data: WebsocketMessage) => {
      if (data.payload.sensor.includes('DHT') && typeof data.payload.value === 'object') {
        data.payload.value =
          data.payload.value.temperature + '°C / ' + data.payload.value.humidity + '%';
      }
      this.sensorData[data.payload.sensor] = data.payload;
    });
  }

  setColorPreset(r: number, g: number, b: number) {
    this.r = r;
    this.g = g;
    this.b = b;
  }

  setColorPresetByName(color: 'red' | 'green' | 'blue') {
    this.color = color;
  }

  sendRgb() {
    // this.rgbService.setRgb(this.r, this.g, this.b).subscribe({
    //   next: () => console.log('RGB set', this.r, this.g, this.b),
    //   error: (e) => console.error('Failed to set RGB', e),
    // });
    this.rgbService.setRgb(this.color).subscribe({
      next: () => console.log('RGB set', this.color),
      error: (e) => console.error('Failed to set RGB', e),
    });
  }
}
