import { TestBed } from '@angular/core/testing';

import { SearchAlertService } from './search-alerts';

describe('SearchAlerts', () => {
  let service: SearchAlertService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SearchAlertService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
