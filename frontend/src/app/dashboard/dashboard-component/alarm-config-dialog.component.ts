import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

@Component({
  selector: 'app-alarm-config-dialog',
  standalone: true,
  imports: [CommonModule, FormsModule, MatDialogModule, MatButtonModule, MatSlideToggleModule],
  template: `
    <h2 mat-dialog-title>Configure Alarm</h2>
    <div mat-dialog-content>
      <p *ngIf="!configKeys.length">No alarm configuration available.</p>
      <div *ngFor="let key of configKeys" class="row">
        <mat-slide-toggle [(ngModel)]="localConfig[key]">{{ prettyLabel(key) }}</mat-slide-toggle>
      </div>
    </div>
    <div mat-dialog-actions style="justify-content: flex-end; gap:8px;">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-flat-button color="primary" (click)="onConfirm()">Confirm</button>
    </div>
  `,
  styles: [`
    .row { padding: 8px 0; }
  `]
})
export class AlarmConfigDialogComponent {
  localConfig: { [key: string]: any } = {};
  configKeys: string[] = [];

  constructor(
    private dialogRef: MatDialogRef<AlarmConfigDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    const cfg = data?.alarm_config || {};
    // shallow copy to avoid mutating original until confirm
    this.localConfig = { ...cfg };
    this.configKeys = Object.keys(this.localConfig);
  }

  prettyLabel(key: string): string {
    // convert snake_case or camelCase to Title Case
    return key.replace(/([A-Z])/g, ' $1')
      .replace(/_/g, ' ')
      .replace(/^./, s => s.toUpperCase());
  }

  onCancel() {
    this.dialogRef.close(null);
  }

  onConfirm() {
    this.dialogRef.close(this.localConfig);
  }
}
