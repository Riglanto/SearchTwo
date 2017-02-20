import { Component, OnInit } from '@angular/core';
import { Observable }       from 'rxjs/Observable';
import { Subject }          from 'rxjs/Subject';
import './../rxjs-operators';

import { Item } from './../item';
import { SearchListService } from './../search-list.service';
import { SharedService }			from './../shared.service';

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
  lastSelected: Item;

  shops = [
    'ebay.de',
    'amazon.de'
  ];

  constructor(private sharedService: SharedService, private searchListService: SearchListService) {
    this.shop = this.shops[0];
    this.leftKeyword = "Batman";
    this.rightKeyword = "Spiderman";
  }

  ngOnInit() {
  }

  searchLeftItems(seller: string): void {
    this.sharedService.loading = true;
    this.searchListService.getItems(this.leftKeyword, seller).then(
      items => {
        this.leftItems = items;
        this.sharedService.loading = false;
      }
    );
  }

  searchRightItems(seller: string): void {
    this.sharedService.loading = true;
    this.searchListService.getItems(this.rightKeyword, seller).then(
      items => {
        this.rightItems = items;
        this.sharedService.loading = false;
      }
    );
  }

  search(): void {
    this.searchLeftItems('');
    this.searchRightItems('');
  }

  getImage(url: string): string {
    return "app/images/image.png";
  }

  onSelectLeftItem(item: Item): void {
    this.selectDeselect(item);
    this.searchRightItems(item.seller);
  }

  onSelectRightItem(item: Item): void {
    this.selectDeselect(item);
    this.searchLeftItems(item.seller);
  }

  selectDeselect(item: Item): void {
    if(this.lastSelected)
      this.lastSelected.selected = false;
    item.selected = true;
    this.lastSelected = item;
  }

}
