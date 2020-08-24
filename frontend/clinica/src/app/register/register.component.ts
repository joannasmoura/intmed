import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { first } from 'rxjs/operators';
import { AuthenticationService } from '../core/services/auth.service';
import { MatDialogConfig, MatDialog } from '@angular/material/dialog';
import { ModalMessageComponent } from '../shared/modal-message/modal-message.component';

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
hidePassword=true;
hideConfirmPassword=true;
passwordMatch:boolean=true;
  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      first_name: ['', [Validators.required]],
      email: ['', [Validators.required,Validators.pattern('^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,4}$')]],      
      password: ['', [Validators.required]],      
      passwordConfirm: ['', [Validators.required]],
    }, {validator: this.matchPassword.bind(this) });
  }
  get first_name() {
    return this.registerForm.get('first_name');
  } 
  get email() {
    return this.registerForm.get('email');
  } 
  get password() {
      return this.registerForm.get('password');
  }
  get passwordConfirm() {
    return this.registerForm.get('passwordConfirm');
  }

  matchPassword(formGroup: FormGroup){
    const password = formGroup.controls['password'];
    const passwordConfirm = formGroup.controls['passwordConfirm'];
    if (passwordConfirm.errors && !passwordConfirm.errors.confirmedValidator) {
        return;
    }
    if (password.value !== passwordConfirm.value) {
        passwordConfirm.setErrors({ confirmedValidator: true });
    } else {
        passwordConfirm.setErrors(null);
    }
  }

  get f() { return this.registerForm.controls; }

  onSubmit() {
    this.error = "";
    if (this.registerForm.invalid) {
        return;
    }    
    let formData = this.registerForm.value
    this.authenticationService.register({...formData, username:formData.email}).pipe(first())
      .subscribe(
          data => {
            this.abrirModalMensagem('Conta criada com sucesso!', true);
          },
          err => {
            if(err.error.username){
              this.error = 'Já existe um usuário cadastrado com esse e-mail';
            }else{
              this.error = err.error.message;
            }
        }
    );
  }

  abrirModalMensagem(message, success) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = {message:message, success:success}
    let dialogRef = this.dialog.open(ModalMessageComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(res =>{
      location.replace('login');
    })
  }

  cancelar(){
    this.router.navigate(['/login']);
  }

}
