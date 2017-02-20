import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppRoutingModule }     from './app-routing.module';

import { AppComponent } from './app.component';
import { SearchListComponent } from './search-list/search-list.component';
import { SearchListService }			from './search-list.service';
import { SharedService }			from './shared.service';

@NgModule({
  declarations: [
    AppComponent,
    SearchListComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
	AppRoutingModule
  ],
  providers: [SharedService, SearchListService],
  bootstrap: [AppComponent]
})
export class AppModule { }
