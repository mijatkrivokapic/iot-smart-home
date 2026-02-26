import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment/environment';

@Injectable({
  providedIn: 'root',
})
export class RgbService {
  constructor(private http: HttpClient) {}

  setRgb(color: string): Observable<any> {
    return this.http.post(`${environment.apiUrl}/api/rgb`, { color });
  }
}
