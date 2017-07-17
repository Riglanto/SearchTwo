import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import './rxjs-operators';

import { Item } from './item';
import { SharedService } from './shared.service';

@Injectable()
export class SearchListService {

  private serverUrl = 'https://searchtwo-backend.appspot-preview.com/items?';
  private localUrl = 'http://localhost:5000/';

  constructor(private http: Http) { }

  getItems(keyword: string, seller: string, shop: string): Promise<Item[]> {
    console.log('getItems' + keyword + seller);
    var url = this.localUrl + 'items?';
    if (keyword != '')
      url += 'keyword=' + keyword + '&';
    if (seller != '')
      url += 'seller=' + seller + '&';
    if (shop != '')
      url += 'shop=' + shop;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json() as Item[])
      .catch(this.handleError);
  }

  getLinks(itemUrl: string): Promise<any> {
    var url = this.localUrl + 'getLinks?';
    url += 'itemUrl=' + itemUrl;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json())
      .catch(this.handleError);
  }

  getPromos(): Promise<any[]> {
    var url = this.localUrl + 'promos';
    return this.http.get(url)
      .toPromise()
      .then(response => response.json()['promos'] as any[])
      .catch(this.handleError);
  }

  private fakeService(error: any) {
    console.log('fakeService');
    var items = [];
    for (let i = 0; i < 10; i++) {
      let item = new Item();
      item.title = "Item #" + i;
      item.price = i * i + '.' + i * 10;
      item.currency = 'USD';
      items.push(item);
    }
    return Promise.resolve(items);
  }

  private handleError(error: any) {
    return Promise.reject(error.json().message || error);
  }
}
