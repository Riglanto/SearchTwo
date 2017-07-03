import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import './../rxjs-operators';

import { Item } from './../item';
import { SearchListService } from './../search-list.service';
import { SharedService } from './../shared.service';

@Component({
  selector: 'app-search-list',
  templateUrl: './search-list.component.html',
  styleUrls: ['./search-list.component.css']
})
export class SearchListComponent implements OnInit {

  searchColumns: number = 3;
  shop: string;
  items: Item[][] = new Array(this.searchColumns);
  sellers: string[] = new Array(this.searchColumns);
  keywords: string[] = new Array(this.searchColumns);
  lastSelected: Item[] = new Array(this.searchColumns);
  hasSearched: boolean = false;

  shops = [
    'ebay.de',
    'amazon.de'
  ];

  constructor(private sharedService: SharedService, private searchListService: SearchListService) {
  }

  ngOnInit() {
    this.shop = this.shops[0];
    this.keywords[0] = "Batman";
    this.keywords[1] = "Spiderman";
    if (this.searchColumns > 2)
      this.keywords[2] = "Superman";
    this.searchColumns = 2;
  }

  searchLeftItems(seller: string): void {
    this.sharedService.loading = true;
    this.searchListService.getItems(this.keywords[0], seller).then(
      items => {
        this.items[0] = items;
        this.sharedService.loading = false;
      }
    );
  }

  searchRightItems(seller: string): void {
    this.sharedService.loading = true;
    this.searchListService.getItems(this.keywords[1], seller).then(
      items => {
        this.items[1] = items;
        this.sharedService.loading = false;
      }
    );
  }

  searchItemsInColumn(column: number, seller = ''): void {
    this.sharedService.loading = true;
    this.searchListService.getItems(this.keywords[column], seller).then(
      items => {
        this.items[column] = items;
        this.sharedService.loading = false;
      }
    );
  }

  search(): void {
    for (let i = 0; i < this.searchColumns; i++) {
      this.searchItemsInColumn(i);
    }
  }

  getImage(url: string): string {
    return "app/images/image.png";
  }

  onSelectItemInColumn(column: number, item: Item) {
    this.selectDeselect(column, item);
  }

  selectDeselect(column: number, item: Item): void {
    var seller = '';
    if (!item.selected) {
      if (this.lastSelected[column]) {
        this.lastSelected[column].selected = false;
      }
      this.lastSelected[column] = item;
      seller = item.seller;
    } else {
      this.lastSelected[column] = null;
    }
    for (let i = 0; i < this.searchColumns; i++) {
      if (i !== column)
        this.searchItemsInColumn(i, seller);
    }
    item.selected = !item.selected;
  }

  searchColumnsList() {
    var x: number[] = [];
    for (let i = 0; i < this.searchColumns; i++) {
      x.push(i);
    }
    return x;
  }

}
