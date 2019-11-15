import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ApiService, IServiceSource} from '../../services/api.service';

@Component({
  selector: 'app-comment-form',
  templateUrl: './comment-form.component.html',
  styleUrls: ['./comment-form.component.scss']
})
export class CommentFormComponent implements OnInit {
  public isSend: boolean;
  public commentForm: FormGroup;
  public formError: boolean;

  constructor(
    private formBuilder: FormBuilder,
    private api: ApiService,
  ) {
  }

  ngOnInit() {
    this.commentForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(64)]],
      comment: ['', [Validators.required, Validators.maxLength(256)]]
    });
  }

  public controlIsInvalid(name: string) {
    return this.commentForm.controls[name].invalid &&
      (this.commentForm.controls[name].dirty || this.commentForm.controls[name].touched);
  }

  private markControlsAsTouched(form) {
    for (let control in form.controls) {
      form.controls[control].markAsTouched();
      form.controls[control].markAsDirty();
      if (form.controls[control].controls) {
        this.markControlsAsTouched(form.controls[control]);
      }
    }
  }

  public invalidText(name: string) {
    const field = this.commentForm.controls[name];

    if (field.errors) {
      if (field.errors.required) {
        return 'Обязательное поле';
      }
      if (field.errors.maxlength) {
        if (name === 'name') {
          return `Максимальная длина имени пользователя - ${field.errors.maxlength.requiredLength} символа.`;
        }
        if (name === 'comment') {
          return `Максимальная длина комментария - ${field.errors.maxlength.requiredLength} символа.`;
        }
      }
    }
  }

  public submit() {
    if (this.commentForm.invalid) {
      this.markControlsAsTouched(this.commentForm);
      return false;
    }
    const comment = {
      user_name: this.commentForm.value.name,
      note: this.commentForm.value.comment
    };
    this.api.sendComment(comment).subscribe((data: IServiceSource) => {
        if (data) {
          this.commentForm.reset();
          this.formError = false;
        }
      },
      error => {
        this.formError = error.statusText;
      });
  }
}
