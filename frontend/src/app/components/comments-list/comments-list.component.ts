import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../services/api.service';

@Component({
  selector: 'app-comments-list',
  templateUrl: './comments-list.component.html',
  styleUrls: ['./comments-list.component.scss']
})
export class CommentsListComponent implements OnInit {
  public comments = [] as any;

  constructor(
    public api: ApiService
  ) { }

  ngOnInit() {
    this.comments = this.api.comments.sort((a, b) => {
      const x = new Date(a.date_time);
      const y = new Date(b.date_time);
      return +x - +y;
    });
  }

  public getHref(id) {
    return `/comment/${id}`;
  }
}
