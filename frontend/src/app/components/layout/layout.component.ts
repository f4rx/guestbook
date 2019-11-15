import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {

  constructor(
    public api: ApiService,
  ) { }

  ngOnInit() {}

  public getColor(id) {
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
      const n = id.charCodeAt(i);
      hash += n;
    }
    return 'hsla(' + hash + ', 50%, 50%, 0.7)';
  }
}
