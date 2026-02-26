import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SensorService {
  constructor(private socket: Socket) {}

  onPi1SensorUpdate(): Observable<any> {
    return this.socket.fromEvent('sensor-data-PI1');
  }

  onPi2SensorUpdate(): Observable<any> {
    return this.socket.fromEvent('sensor-data-PI2');
  }

  onPi3SensorUpdate(): Observable<any> {
    return this.socket.fromEvent('sensor-data-PI3');
  }
}
