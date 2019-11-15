import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { WorkshopComponent } from './components/workshop/workshop.component';
import { CommentComponent } from './components/comment/comment.component';


const routes: Routes = [
  {
    path: '',
    component: WorkshopComponent,
  },
  {
    path: 'comment/:key',
    component: CommentComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
