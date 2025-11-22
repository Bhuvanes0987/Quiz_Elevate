import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private baseUrl = 'http://localhost:8000/api/users'; // change if needed

  constructor(private http: HttpClient) {}

  getUsers(page: number, limit: number, search: string): Observable<any> {
    let params = new HttpParams()
      .set('page', page)
      .set('limit', limit)
      .set('search', search);

    return this.http.get<any>(this.baseUrl, { params });
  }
}
