import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SearchAlertResponse } from './interfaces/search-alerts/search-alert-response';
import { SearchAlertRequest } from './interfaces/search-alerts/search-alert-request';

@Injectable({
  providedIn: 'root'
})
export class SearchAlertService {
  apiUrl = environment.backendApiUrl + '/search-alerts'

  constructor(private http: HttpClient) { }

/**
 * Fetches a list of search alerts from the backend API.
 *
 * @param limit - The maximum number of search alerts to retrieve.
 * @param offset - The number of search alerts to skip before starting to collect the result set.
 * @returns An observable containing an array of search alert responses.
 */
  getSearchAlerts(limit: number, offset: number): Observable<SearchAlertResponse[]> {
    return this.http.get<SearchAlertResponse[]>(`${this.apiUrl}/?limit=${limit}&offset=${offset}`);
  }

  /**
   * Sends a POST request to the backend API to create a new search alert.
   *
   * @param request - The search alert request object containing the job area and state.
   * @returns An observable with a response containing the newly created search alert.
   */
  createSearchAlert(request: SearchAlertRequest): Observable<SearchAlertResponse> {
    return this.http.post<SearchAlertResponse>(this.apiUrl, request);
  }

  /**
   * Retrieves a specific search alert from the backend API using its ID.
   *
   * @param id - The unique identifier of the search alert to retrieve.
   * @returns An observable containing the search alert response.
   */
  getSearchAlert(id: number): Observable<SearchAlertResponse> {
    return this.http.get<SearchAlertResponse>(`${this.apiUrl}/${id}`);
  }

  /**
   * Deletes a search alert with the given ID from the backend API.
   *
   * @param id - The unique identifier of the search alert to delete.
   * @returns An observable that signals when the deletion is complete.
   */
  deleteSearchAlert(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
