import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../environment/environment';

@Injectable({
  providedIn: 'root',
})
export class TimerService {
  constructor(private http:HttpClient) {}

  startTimer(duration: number): Observable<any> {
    return this.http.post(`${environment.apiUrL}/api/timer/start`,{'time':duration});
  }

  setTimerIncrement(increment: number): Observable<any> {
    return this.http.put(`${environment.apiUrL}/api/timer/config`, { 'time' : increment });
  }

  incrementTimer(): Observable<any> {
    return this.http.post(`${environment.apiUrL}/api/timer/increment`, {});
  }

}
