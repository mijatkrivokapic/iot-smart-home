import { Injectable } from '@angular/core';
import {Socket} from 'ngx-socket-io';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SystemStateService {
  constructor(private socket: Socket) {}

  onStateUpdate(): Observable<any> {
    return this.socket.fromEvent('state-update');
  }
}
