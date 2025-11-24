import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

private baseUrl = 'http://localhost:8000/users';

  constructor(private http: HttpClient) {}

  getUsers(): Observable<any> {
    return this.http.get<any>(this.baseUrl);
  }
  // Soft delete user by setting is_active = 0
softDeleteUser(userId: number): Observable<any> {
  return this.http.put<any>(`${this.baseUrl}/${userId}/delete`, {}); 
}

}
