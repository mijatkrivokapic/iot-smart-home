import {Component, OnInit} from '@angular/core';
import {SensorData, WebsocketMessage} from '../../models/sensor-data';
import {SensorService} from '../../services/sensor-service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {MatCardModule} from '@angular/material/card';
import {MatTableModule} from '@angular/material/table';
import {TimerService} from '../../services/timer-service';
import {MatDialog, MatDialogModule} from '@angular/material/dialog';
import {TimerDialogComponent} from './timer-dialog.component';

@Component({
  selector: 'app-pi2-dashboard',
  imports: [CommonModule, FormsModule, MatCardModule, MatTableModule, MatDialogModule],
  templateUrl: './pi2-dashboard.html',
  styleUrls: ['./pi2-dashboard.scss'],
  standalone: true
})
export class Pi2Dashboard implements OnInit {
  sensorData: { [key: string]: any } = {};
  displayTime: string = '00:00';
  isBlinking: boolean = false;

  constructor(private sensorService: SensorService,
              private timerService:TimerService,
              private dialog: MatDialog) {}

  ngOnInit(): void {
    this.sensorService.onPi2SensorUpdate().subscribe((data: any) => {
      if(data.payload.sensor === '4SD'){
        const value = JSON.parse(data.payload.value);
        this.isBlinking = value['is_blinking'];
        this.displayTime = this.formatTime(value['current_time']);
      }
      else
        this.sensorData[data.payload.sensor] = data.payload;
    })
  }

  private formatTime(totalSeconds: number): string {
    const minutes: number = Math.floor(totalSeconds / 60);
    const seconds: number = totalSeconds % 60;

    const mStr = String(minutes).padStart(2, '0');
    const sStr = String(seconds).padStart(2, '0');

    return `${mStr}:${sStr}`;
  }

  start_timer(){
    const ref = this.dialog.open(TimerDialogComponent, {width: '600px'});
    ref.afterClosed().subscribe((result: number | null) => {
      if(result && result > 0){
        this.timerService.startTimer(result).subscribe({
          next: () => {
            console.log('Timer started', result);
          },
          error: () => {
            console.error('Failed to start timer');
          }
        });
      }
    });
  }
}
