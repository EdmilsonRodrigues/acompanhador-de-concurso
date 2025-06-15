import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { catchError, Observable, tap, throwError } from 'rxjs';
import { SubscriptionResponse } from './interfaces/subscriptions/subscription-response';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { CheckoutSessionRequest } from './interfaces/subscriptions/checkout-session-request';

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  apiUrl = environment.backendApiUrl + '/subscriptions'

  constructor(private http: HttpClient) { }


  /**
   * Fetches the user's subscription object from the API.
   *
   * @returns An observable that contains the subscription response.
   */
  get(): Observable<SubscriptionResponse> {
    return this.http.get<SubscriptionResponse>(this.apiUrl + '/me');
  }

  /**
   * Posts a request to the API to create a new checkout session
   * and redirects the user to the resulting Stripe Checkout URL.
   *
   * @param request - The request object that contains the subscription
   *                  and price information.
   *
   * @returns An observable that contains the redirect URL.
   */
  goToCheckoutSession(request: CheckoutSessionRequest) {
    const checkoutEndpoint = `${this.apiUrl}/checkout`;

    const response = this.http.post(checkoutEndpoint, request, {
      observe: 'response',
      responseType: 'text'
    })

    return this.redirectResponse('checkout session', response);
 }

  /**
   * Sends a GET request to the API to create a new portal session
   * and redirects the user to the resulting Stripe Billing Portal URL.
   *
   * @returns An observable that contains the redirect URL.
   */
  goToPortalSession() {
    const portalEndpoint = `${this.apiUrl}/portal`;

    const response = this.http.get(portalEndpoint, {
      observe: 'response',
      responseType: 'text'
    })

    return this.redirectResponse('portal session', response);
  }

  /**
   * Intercepts an HTTP response and redirects the user to the
   * URL present in the Location header if the status is 303.
   *
   * @param logName - The name of the thing being redirected to,
   *                  for logging purposes.
   * @param response - The Observable<HttpResponse<any>> to intercept.
   *
   * @returns An Observable that completes when the redirect is initiated,
   *          or an error if the response status is not 303, or there is
   *          no Location header present in the response.
   */
  private redirectResponse(logName: string, response: Observable<HttpResponse<any>>): Observable<HttpResponse<any>> {
    return response.pipe(
      tap((response: HttpResponse<any>) => {
        if (response.status === 303) {
          const redirectUrl = response.headers.get('Location');
          if (redirectUrl) {
            console.log(`Redirecting to ${logName}:`, redirectUrl);
            window.location.href = redirectUrl;
            return;
          } else {
            console.error('303 redirect received, but no Location header found.');
            throw new Error('Redirect URL missing from response.');
          }
        } else {
          console.warn(`Unexpected status ${response.status} for ${logName}.`, response.body);
        }
      }),
      catchError(error => {
        console.error(`Error initiating ${logName}:`, error);
        return throwError(() => new Error(`Failed to initiate ${logName}.`));
      })
    );

  }
}
