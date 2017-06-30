import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import './rxjs-operators';

import { Item } from './item';

@Injectable()
export class SearchListService {

  private serverUrl = 'https://searchtwo-backend.appspot-preview.com/items?';
  private localUrl = 'http://localhost:5000/items?';

  constructor(private http: Http) { }

    getItems(keyword: string, seller: string): Promise<Item[]> {
    console.log('getItems' + keyword + seller);
    var url = this.localUrl;
    if(keyword != '')
        url += 'keyword=' + keyword + '&';
    if(seller != '')
        url += 'seller=' + seller;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Item[])
      .catch(this.handleError);
  }

  private handleError(error: any) {
    Promise.resolve();
  }
}
