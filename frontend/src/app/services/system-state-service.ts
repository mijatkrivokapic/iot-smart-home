import { Injectable } from '@angular/core';
import {Socket} from 'ngx-socket-io';
import {Observable} from 'rxjs';
import {environment} from '../environment/environment';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class SystemStateService {
  constructor(private socket: Socket, private http:HttpClient) {}

  onStateUpdate(): Observable<any> {
    return this.socket.fromEvent('state-update');
  }

  getCurrentState(): Observable<any> {
    return this.http.get<Observable<any>>(`${environment.apiUrl}/api/state`);
  }
}
