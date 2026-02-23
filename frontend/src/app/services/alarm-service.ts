import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { environment } from '../environment/environment';

@Injectable({
  providedIn: 'root',
})
export class AlarmService {
  constructor(private http: HttpClient) {}

  submitPassword(password: string): Observable<any> {
    const payload = { password };
    return this.http.post(`${environment.apiUrl}/api/password`, payload);
  }
}
