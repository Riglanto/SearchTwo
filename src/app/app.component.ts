import { Component } from '@angular/core';
import { SharedService }			from './shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  title: string = 'Search two';

  constructor(public sharedService: SharedService) {
  }
}
