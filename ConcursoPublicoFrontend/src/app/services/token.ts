import { Injectable } from '@angular/core';
import { BehaviorSubject, catchError, Observable, tap, throwError } from 'rxjs';
import { TokenData } from './interfaces/auth/token-data';
import { AuthService } from './auth';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class TokenService {
  private accessTokenSubject = new BehaviorSubject<string | null>(null);
  public accessToken$ = this.accessTokenSubject.asObservable();

  constructor(private authService: AuthService, private router: Router) {
    this.checkTokenOnAppLoad();
  }

  get accessToken(): string | null {
    return this.accessTokenSubject.value;
  }

  isAuthenticated(): boolean {
    return !!this.accessTokenSubject.value;
  }

  authenticate(loginResponse: Observable<TokenData>): Observable<TokenData> {
    return loginResponse.pipe(
      tap(tokenData => {
        this.setAccessToken(tokenData.accessToken);
      }),
      catchError(error => {
        console.error('Login failed:', error);
        this.clearTokens();
        return throwError(() => error);
      })
    )
  }

  refreshAccessToken(): Observable<TokenData> {
    return this.authService.refresh().pipe(
      tap(tokenData => {
        this.setAccessToken(tokenData.accessToken);
      }),
      catchError(error => {
        console.error('Refresh token failed:', error);
        this.clearTokens();
        this.router.navigate(['/login']);
        return throwError(() => error);
      })
    )
  }

  logout(): void {
    this.clearTokens();
  }

  private setAccessToken(token: string): void {
    this.accessTokenSubject.next(token);
    console.log('Access Token updated in memory.');
  }

  private clearTokens(): void {
    this.accessTokenSubject.next(null);
    console.log('Access Token cleared from memory.');
  }

  private checkTokenOnAppLoad(): void {
    this.refreshAccessToken().subscribe({
      next: () => console.log('Session restored via refresh token.'),
      error: () => console.log('No active session or refresh token expired, user needs to login.'),
      complete: () => { }
    });
  }

}
