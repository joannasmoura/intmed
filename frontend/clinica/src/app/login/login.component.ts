import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { AuthenticationService } from '../core/services/auth.service';
import { User } from '../core/models/user';


@Component({ 
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'] 
})
export class LoginComponent implements OnInit {
    loginForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;
    error = '';
    labelAcessar = "Acessar";
    labelCriar = "Criar Conta";
    primary = "primary";
    secondary = "secondary";
    hide = true;

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService
    ) { 
        // redirect to home if already logged in
        if (this.authenticationService.currentUserValue) { 
            this.router.navigate(['/']);
        }
    }

    ngOnInit() {
        this.loginForm = this.formBuilder.group({
            username: ['', Validators.required, Validators],
            password: ['', Validators.required],
            lembrarSenha: [false, Validators.required]
        });

        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    get username() {
        return this.loginForm.get('username');
    }
    get password() {
        return this.loginForm.get('password');
    }

    public errorMessages = {
        username: [
          { type: 'required', message: 'Por favor, digite um e-mail ou login' },
        ],
        password: [
          { type: 'required', message: 'Por favor, digite uma senha' },
        ],
    };


    get f() { return this.loginForm.controls; }

    onSubmit() {
        this.submitted = true;
        if (this.loginForm.invalid) {
            return;
        }

        this.loading = true;
        this.authenticationService.login(this.loginForm.value).subscribe(
            data => {
                this.router.navigate([this.returnUrl]);
            },
            err => {       
                if(err.status == 401){
                    this.error = "Usuário ou senha incorretos."
                }else{
                    this.error = err.error.message;
                }    
            }
        );
    }

    criar(){
        this.router.navigate(['/register']);
    }
}