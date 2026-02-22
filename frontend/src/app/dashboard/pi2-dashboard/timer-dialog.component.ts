import {Component, Inject} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-timer-dialog',
  standalone: true,
  imports: [CommonModule, FormsModule, MatDialogModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>Start Timer</h2>
    <div mat-dialog-content>
      <div class="row">
        <mat-form-field appearance="outline">
          <mat-label>Minutes</mat-label>
          <input matInput type="number" [(ngModel)]="minutes" min="0">
        </mat-form-field>
      </div>
      <div class="row">
        <mat-form-field appearance="outline">
          <mat-label>Seconds</mat-label>
          <input matInput type="number" [(ngModel)]="seconds" min="0" max="59">
        </mat-form-field>
      </div>
      <div class="msg" *ngIf="message">{{ message }}</div>
    </div>
    <div mat-dialog-actions style="justify-content: flex-end; gap:8px;">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-flat-button color="primary" (click)="onStart()">Start</button>
    </div>
  `,
  styles: [`
    .row { margin-bottom: 12px; }
    .msg { color: red; margin-top: 8px; }
    mat-form-field { width: 100%; }
  `]
})
export class TimerDialogComponent {
  minutes: number | null = 0;
  seconds: number | null = 0;
  message: string | null = null;

  constructor(
    private dialogRef: MatDialogRef<TimerDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  onCancel(){
    this.dialogRef.close(null);
  }

  onStart(){
    const m = Number(this.minutes) || 0;
    const s = Number(this.seconds) || 0;

    if(m < 0 || s < 0 || s >= 60){
      this.message = 'Please enter valid minutes and seconds (0-59).';
      return;
    }

    const totalSeconds = m * 60 + s;
    if(totalSeconds <= 0){
      this.message = 'Please enter a duration greater than 0.';
      return;
    }

    this.dialogRef.close(totalSeconds);
  }
}
