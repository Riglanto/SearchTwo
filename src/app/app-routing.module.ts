import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SearchListComponent } from './search-list/search-list.component';

const routes: Routes = [
  { path: '', redirectTo: '/searchlist', pathMatch: 'full' },
  { path: 'searchlist', component: SearchListComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
  
export class AppRoutingModule { }