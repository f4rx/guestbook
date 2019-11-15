import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ApiService, IServiceSource} from '../../services/api.service';

@Component({
  selector: 'app-comment',
  templateUrl: './comment.component.html',
  styleUrls: ['./comment.component.scss']
})
export class CommentComponent implements OnInit {
  public isLoading: boolean;
  public isError: boolean;
  public comment;

  constructor(
    private activatedRoute: ActivatedRoute,
    public api: ApiService
  ) { }

  ngOnInit() {
    this.isLoading = true;
    const key = this.activatedRoute.snapshot.paramMap.get('key');
    this.api.getComment(key).subscribe((data: IServiceSource) => {
        this.comment = data.result;
        this.isLoading = false;
      },
      error => {
        this.isError = error.statusText;
      });
  }
}
