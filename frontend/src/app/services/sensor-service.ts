import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SensorService {
  constructor(private socket: Socket) {}

  onSensorUpdate(): Observable<any> {
    return this.socket.fromEvent('sensor_update');
  }
}
