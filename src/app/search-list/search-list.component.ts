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
  labels: string[] = new Array(this.searchColumns);
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
    this.keywords[0] = "watch";
    this.keywords[1] = "Spiderman";
    if (this.searchColumns > 2)
      this.keywords[2] = "Superman";
    for (let i = 0; i < this.searchColumns; i++)
      this.items[i] = [];
    this.searchColumns = 2;
  }

  searchItemsInColumn(column: number, seller = ''): void {
    this.sharedService.loading = true;
    this.items[column].length = 0;
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
    this.labels = this.keywords.slice(0);
    setTimeout(function() {
      const element = document.querySelector("#results-area");
      if (element) {
        element.scrollIntoView();
      }
    }, 750);
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

  getBgImageStyle(item: Item) {
    const bgImgUrl = item.galleryURL == null && 'assets/image.png' || item.galleryURL;
    return `url(${bgImgUrl})`;
  }

  getSelectedLabel(column: number) {
    return this.lastSelected[column] && ` : ${this.trimTitle(this.lastSelected[column].title)}`;
  }

  trimTitle(text: string) {
    return text.length > 25 ? text.substring(0, 25) + "..." : text;
  }
}
