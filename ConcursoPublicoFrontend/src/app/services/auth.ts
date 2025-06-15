import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { SigninRequest } from './interfaces/auth/signin-request';
import { Observable } from 'rxjs';
import { LoginRequest } from './interfaces/auth/login-request';
import { TokenData } from './interfaces/auth/token-data';
import { RefreshRequest } from './interfaces/auth/refresh-request';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.backendApiUrl + '/auth';

  constructor(private http: HttpClient) { }

  /**
   * Sends a sign-in request to the backend API.
   *
   * @param request - The sign-in request object containing user credentials.
   * @returns An observable with a response indicating the success of the sign-in operation.
   */
  signin(request: SigninRequest): Observable<{ success: boolean }> {
    return this.http.post<{ success: boolean }>(this.apiUrl + '/signin', request);
  }

  /**
   * Sends a login request to the backend API.
   *
   * @param request - The login request object containing user credentials.
   * @returns An observable with a response containing the authentication tokens.
   */
  login(request: LoginRequest): Observable<TokenData> {
    let body = new HttpParams();
    body = body.set('username', request.username);
    body = body.set('password', request.password);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post<TokenData>(this.apiUrl + '/login', body, { headers: headers, withCredentials: true });
  }

  /**
   * Sends a refresh request to the backend API.
   *
   * @param request - The refresh request object containing the refresh token.
   * @returns An observable with a response containing the new authentication tokens.
   */
  refresh(): Observable<TokenData> {
    const body = new HttpParams().set('grant_type', 'refresh_token');

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post<TokenData>(this.apiUrl + '/refresh', body, { headers: headers, withCredentials: true })
  }
}
