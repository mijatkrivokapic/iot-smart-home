import { Component, OnInit } from '@angular/core';
import { SensorService } from '../../services/sensor-service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { TimerService } from '../../services/timer-service';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { TimerDialogComponent } from './timer-dialog.component';
import { IncrementDialogComponent } from './increment-dialog.component';
import { SystemStateService } from '../../services/system-state-service';

@Component({
  selector: 'app-pi2-dashboard',
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatTableModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './pi2-dashboard.html',
  styleUrls: ['./pi2-dashboard.scss'],
  standalone: true,
})
export class Pi2Dashboard implements OnInit {
  sensorData: { [key: string]: any } = {};
  displayTime: string = '00:00';
  isBlinking: boolean = false;
  state: any = null;

  constructor(
    private sensorService: SensorService,
    private timerService: TimerService,
    private systemStateService: SystemStateService,
    private dialog: MatDialog,
  ) {}

  ngOnInit(): void {
    this.sensorService.onPi2SensorUpdate().subscribe((data: any) => {
      if (data.payload.sensor === '4SD') {
        const value = JSON.parse(data.payload.value);
        this.isBlinking = value['is_blinking'];
        this.displayTime = this.formatTime(value['current_time']);
      } else if (data.payload.sensor.includes('DHT') && typeof data.payload.value === 'object') {
        data.payload.value =
          data.payload.value.temperature + '°C / ' + data.payload.value.humidity + '%';
        this.sensorData[data.payload.sensor] = data.payload;
      } else {
        this.sensorData[data.payload.sensor] = data.payload;
      }
    });

    this.systemStateService.onStateUpdate().subscribe((data) => {
      this.state = data;
    });

    this.systemStateService.getCurrentState().subscribe((data) => {
      this.state = data;
      console.log('Current state:', this.state);
    });
  }

  // helper to format seconds as mm:ss
  formatTime(totalSeconds: number): string {
    const minutes: number = Math.floor(totalSeconds / 60);
    const seconds: number = totalSeconds % 60;

    const mStr = String(minutes).padStart(2, '0');
    const sStr = String(seconds).padStart(2, '0');

    return `${mStr}:${sStr}`;
  }

  // Open Angular Material dialog to start timer
  start_timer() {
    const ref = this.dialog.open(TimerDialogComponent, { width: '600px' });
    ref.afterClosed().subscribe((result: number | null) => {
      if (result && result > 0) {
        this.timerService.startTimer(result).subscribe({
          next: () => {
            console.log('Timer started', result);
          },
          error: () => {
            console.error('Failed to start timer');
          },
        });
      }
    });
  }

  // Open dialog to edit increment
  editIncrement() {
    const current = this.state?.timer_increment || 0;
    const ref = this.dialog.open(IncrementDialogComponent, { width: '420px', data: { current } });
    ref.afterClosed().subscribe((result: number | null) => {
      if (result && result > 0) {
        this.timerService.setTimerIncrement(result).subscribe({
          next: () => {
            console.log('Increment set to', result);
          },
          error: () => {
            console.error('Failed to set increment');
          },
        });
      }
    });
  }

  // Ask server to increment timer by configured increment
  incrementTimer() {
    this.timerService.incrementTimer().subscribe({
      next: () => {
        console.log('Requested server to increment timer');
      },
      error: () => {
        console.error('Failed to increment timer');
      },
    });
  }
}
