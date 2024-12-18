import { Injectable, inject } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { History } from '../../interfaces/history';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private http: HttpClient = inject(HttpClient);

  constructor() { }

  getHistoryList(): Observable<History> {
    const historyURL: string = `${environment.apiUrl}/history`;
    return this.http.get<History>(historyURL);
  }

  getHistoryItem(id: number): Observable<History> {
    const historyURL: string = `${environment.apiUrl}/history/${id}`;
    return this.http.get<History>(historyURL);
  }
}
