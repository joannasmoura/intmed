import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { first } from 'rxjs/operators';
import { AuthenticationService } from '../core/services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
registerForm: FormGroup;
primary = "primary";
secondary = "secondary";
error = '';
labelConfirmar="Confirmar"
labelCancelar="Cancelar"
  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService
  ) { }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      nome: ['', Validators.required],
      email: ['', Validators.required],      
      password: ['', Validators.required],      
      passwordConfirm: ['', Validators.required],
  });
  }

  onSubmit() {
    if (this.registerForm.invalid) {
        return;
    }
    let formData = this.registerForm.value
    this.authenticationService.register({...formData, username:formData.email})
        .pipe(first())
        .subscribe(
            data => {
              console.log('criou');
            },
            error => {
                console.log(error);
            }
        );
  }

cancelar(){
  this.router.navigate(['/login']);
}

}
