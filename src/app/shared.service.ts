import { Injectable } from '@angular/core';

@Injectable()
export class SharedService {
  loading = false;
  alert = {
    title: '',
    text: '',
    link: '',
    show: false
  };

  popAlert(title: string, text: string, link = '') {
    this.alert.title = title;
    this.alert.text = text;
    this.alert.link = link;
    this.alert.show = true;
    setTimeout(() => {
      this.alert.show = false;
    }, 3000);
  }
}
