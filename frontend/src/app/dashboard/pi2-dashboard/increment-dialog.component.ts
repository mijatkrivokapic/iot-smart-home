import {Component, Inject} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-increment-dialog',
  standalone: true,
  imports: [CommonModule, FormsModule, MatDialogModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>Edit Timer Increment</h2>
    <div mat-dialog-content>
      <p>Current increment: {{ formatTime(data?.current || 0) }} (mm:ss)</p>
      <mat-form-field appearance="outline">
        <mat-label>Minutes</mat-label>
        <input matInput type="number" [(ngModel)]="minutes" min="0">
      </mat-form-field>
      <mat-form-field appearance="outline">
        <mat-label>Seconds</mat-label>
        <input matInput type="number" [(ngModel)]="seconds" min="0" max="59">
      </mat-form-field>
      <div class="msg" *ngIf="message">{{ message }}</div>
    </div>
    <div mat-dialog-actions style="justify-content: flex-end; gap:8px;">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-flat-button color="primary" (click)="onSave()">Save</button>
    </div>
  `,
  styles: [`
    mat-form-field { width: 100%; display:block; margin-bottom:8px; }
    .msg { color: red; margin-top: 8px; }
  `]
})
export class IncrementDialogComponent {
  minutes: number | null = 0;
  seconds: number | null = 0;
  message: string | null = null;

  constructor(
    private dialogRef: MatDialogRef<IncrementDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ){
    const current = Number(data?.current) || 0;
    this.minutes = Math.floor(current/60);
    this.seconds = current % 60;
  }

  formatTime(totalSeconds: number): string {
    const m = Math.floor(totalSeconds/60);
    const s = totalSeconds % 60;
    return String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
  }

  onCancel(){ this.dialogRef.close(null); }

  onSave(){
    const m = Number(this.minutes) || 0;
    const s = Number(this.seconds) || 0;
    if(m < 0 || s < 0 || s >= 60){
      this.message = 'Please enter valid minutes and seconds (0-59).';
      return;
    }
    const total = m*60 + s;
    if(total <= 0){ this.message = 'Increment must be greater than 0.'; return; }
    this.dialogRef.close(total);
  }
}
