import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {BehaviorSubject} from 'rxjs';
import {tap} from 'rxjs/operators';

export interface IServiceSource {
  host_name: string;
  result: any;
}

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  public isLoading: boolean;
  public isError = false;
  public hostName: string;
  public comments = [] as any;

  public comments$ = new BehaviorSubject([]);

  constructor(
    private http: HttpClient
  ) {
    this.fetchServerInfo();
  }
  private updateServerInfo(info: IServiceSource) {
    this.hostName = info.host_name;
    this.comments = info.result;
    this.comments$.next(this.comments);
  }

  public fetchServerInfo() {
    this.isLoading = true;
    return this.http.get(`http://${location.hostname}:80/notes`).subscribe(
      (data: IServiceSource) => {
        this.updateServerInfo(data);
        this.isLoading = false;
      },
      error => {
        this.isError = error.statusText;
      }
    );
  }

  public getComment(id: string) {
    return this.http.get(`http://${location.hostname}:80/note/${id}`);
  }

  public sendComment(comment) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };
    return this.http
      .post(`http://${location.hostname}:80/note`, comment, httpOptions)
      .pipe(tap((res: IServiceSource) => {
        const comments = this.comments.slice(0);
        comments.push(res.result);

        this.comments = comments;
        this.comments$.next(comments);
      }));
  }
}
