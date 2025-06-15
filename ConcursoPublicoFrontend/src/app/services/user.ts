import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { UserResponse } from './interfaces/users/user-response';
import { UserUpdateRequest } from './interfaces/users/user-update-request';
import { UserUpdatePasswordRequest } from './interfaces/users/user-update-password-request';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  apiUrl = environment.backendApiUrl + '/me'

  constructor(private http: HttpClient) { }

  /**
   * Fetches the current user from the backend API.
   *
   * @returns An observable containing the user response.
   */
  get(): Observable<UserResponse> {
    return this.http.get<UserResponse>(this.apiUrl);
  }

  /**
   * Updates the current user with the given request.
   *
   * @param request - A `UserUpdateRequest` or `UserUpdatePasswordRequest` object containing the new user data.
   * @returns An observable containing the updated user response.
   */
  update(request: UserUpdateRequest | UserUpdatePasswordRequest): Observable<UserResponse> {
    return this.http.patch<UserResponse>(this.apiUrl, request);
  }

  /**
   * Deletes the current user from the backend API.
   *
   * @returns An observable that signals when the deletion is complete.
   */
  delete(): Observable<void> {
    return this.http.delete<void>(this.apiUrl);
  }
}
