import { Component, OnInit } from '@angular/core';
import { Observable }       from 'rxjs/Observable';
import { Subject }          from 'rxjs/Subject';
import './../rxjs-operators';

import { Item } from './../item';
import { SearchListService } from './../search-list.service';

@Component({
  selector: 'app-search-list',
  templateUrl: './search-list.component.html',
  styleUrls: ['./search-list.component.css']
})
export class SearchListComponent implements OnInit {

  shop: string;
  leftItems: Item[];
  rightItems: Item[];
  leftSeller: string;
  rightSeller: string;
  leftKeyword: string;
  rightKeyword: string;

  shops = [
    'ebay.de',
    'amazon.de'
  ];

  constructor(private searchListService: SearchListService) {
    this.shop = this.shops[0];
    this.leftKeyword = "Batman";
    this.rightKeyword = "Spiderman";
  }

  ngOnInit() {
  }

  searchLeftItems(seller: string): void {
    this.searchListService.getItems(this.leftKeyword, seller).then(items => this.leftItems = items);
  }

  searchRightItems(seller: string): void {
    this.searchListService.getItems(this.rightKeyword, seller).then(items => this.rightItems = items);
  }

  search(): void {
    this.searchLeftItems('');
    this.searchRightItems('');
  }

  getImage(url: string): string {
    return "app/images/image.png";
  }

  onSelectLeftItem(item: Item): void {
    this.searchRightItems(item.seller);
  }

  onSelectRightItem(item: Item): void {
    this.searchLeftItems(item.seller);
  }

}
