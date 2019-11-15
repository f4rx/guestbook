import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HeaderModule, NFormsModule, NotificationModule} from 'carbon-components-angular';
import { WorkshopComponent } from './components/workshop/workshop.component';
import { ReactiveFormsModule } from '@angular/forms';
import { CommentComponent } from './components/comment/comment.component';
import { LayoutComponent } from './components/layout/layout.component';
import { CommentFormComponent } from './components/comment-form/comment-form.component';
import { CommentsListComponent } from './components/comments-list/comments-list.component';

@NgModule({
  declarations: [
    AppComponent,
    WorkshopComponent,
    CommentComponent,
    LayoutComponent,
    CommentFormComponent,
    CommentsListComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    HeaderModule,
    NFormsModule,
    ReactiveFormsModule,
    NotificationModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
