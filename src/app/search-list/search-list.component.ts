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
  styleUrls: ['./search-list.component.scss']
})
export class SearchListComponent implements OnInit {

  searchColumns: number = 3;
  selectedShop: string;
  items: Item[][] = new Array(this.searchColumns);
  sellers: string[] = new Array(this.searchColumns);
  keywords: string[] = new Array(this.searchColumns);
  labels: string[] = new Array(this.searchColumns);
  lastSelected: Item[] = new Array(this.searchColumns);
  isInputFocused: boolean[] = new Array(this.searchColumns);
  hasSearched: boolean = false;
  promos: any[];

  shops = [
    'ebay.us',
    'ebay.gb',
    'ebay.de',
    'amazon.de',
    'allegro.pl'
  ];

  constructor(private sharedService: SharedService, private searchListService: SearchListService) {
  }

  ngOnInit() {
    this.selectedShop = this.shops[0];
    this.keywords[0] = "watch";
    this.keywords[1] = "Spiderman";
    this.keywords[2] = "Superman";
    for (let i = 0; i < this.searchColumns; i++)
      this.items[i] = [];
    this.isInputFocused.fill(false);
    this.searchColumns = 2;
    this.searchListService.getPromos().then(
      promos => this.promos = promos
    );
  }

  searchItemsInColumn(column: number, seller = ''): void {
    this.sharedService.loading += 1;
    this.items[column].length = 0;
    this.searchListService.getItems(this.keywords[column], seller, this.selectedShop).then(
      items => {
        this.items[column] = items;
        this.sharedService.loading -= 1;
        this.hasSearched = true;
      }
    ).catch(error => {
      this.sharedService.popAlert('Error', error);
      this.sharedService.loading -= 1;
      this.hasSearched = false;
    });
  }

  search(): void {
    for (let i = 0; i < this.searchColumns; i++) {
      this.searchItemsInColumn(i);
    }
    this.labels = this.keywords.slice(0);
    this.waitAndScroll()
  }

  waitAndScroll() {
    setTimeout(() => {
      if (!this.sharedService.loading) {
        const element = document.querySelector("#mobile-results");
        if (element) {
          element.scrollIntoView();
        }
      } else {
        this.waitAndScroll();
      }
    }, 250);
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
      if (i !== column) {
        this.searchItemsInColumn(i, seller);
        this.sellers[i] = seller;
      }
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

  clearKeyword(column: number) {
    this.keywords[column] = '';
  }

  addToCart(item: Item) {
    this.searchListService.getLinks(item.viewItemURL).then(
      page => {
        this.navigateTo(page['cart']);
      }
    );
  }

  navigateTo(url: string) {
    var win = window.open(url, "_blank");
    if (!win) {
      this.sharedService.popAlert('Popup blocked', 'Here is the ', url);
    }
  }

  showInfo(info) {
    console.log(info);
  }

  searchPromo(promo) {
    this.searchColumns = promo.keywords.length;
    for (let i = 0; i < this.searchColumns; i++)
      this.keywords[i] = promo.keywords[i];
    this.search();
  }
}
