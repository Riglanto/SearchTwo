/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { SearchListService } from './search-list.service';

describe('SearchListService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SearchListService]
    });
  });

  it('should ...', inject([SearchListService], (service: SearchListService) => {
    expect(service).toBeTruthy();
  }));
});
