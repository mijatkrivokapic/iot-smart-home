import { Component, OnInit } from '@angular/core';
import { SensorService } from '../../services/sensor-service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard-component',
  imports: [CommonModule],
  templateUrl: './dashboard-component.html',
  styleUrl: './dashboard-component.scss',
})
export class DashboardComponent implements OnInit {
  sensors: any[] = [];

  constructor(private sensorService: SensorService) {}
  
  
  ngOnInit(): void {
    this.sensorService.onSensorUpdate().subscribe((data) => {
      this.sensors.push(data);
    });
  }
}
