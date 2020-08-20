import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map,tap } from 'rxjs/operators';
import { JwtHelperService } from "@auth0/angular-jwt";
import { environment } from '../../../environments/environment';
import { User } from '../models/user';
import { AuthResponse } from '../models/auth-response';

const helper = new JwtHelperService();
@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private authState: BehaviorSubject<User>;
    public currentUser: Observable<User>;

    constructor(private http: HttpClient) {
        this.authState = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
        this.currentUser = this.authState.asObservable();
    }    

    public get currentUserValue(): User {
        return this.authState.value;
    }

    login(user:User) {
        return this.http.post(`${environment.apiUrl}/login/`, user)
            .pipe(
                tap(async (res: AuthResponse) => {
                    if (res.access) {
                        let payload = helper.decodeToken(res.access)
                        let user = {username:payload.username, firstName:payload.firstName, id:payload.id} 
                        localStorage.setItem('access_token', res.access)
                        localStorage.setItem('refresh_token', res.refresh)
                        localStorage.setItem('currentUser', JSON.stringify(user));
                        this.authState.next(user);
                        return user;
                    }
                })
            );
    }

    register(user:User) {
        return this.http.post(`${environment.apiUrl}/registrar/`, user)
            .pipe(
                tap(async (res: AuthResponse) => {
                    console.log(res)
                    // if (res.token) {
                    //     user.token = res.token
                    //     let decoded = helper.decodeToken(res.token); 
                    //     localStorage.setItem('currentUser', JSON.stringify(decoded));
                    //     this.authState.next(user);
                    //     return user;
                    // }
                })
            );
    }

    refreshToken(){
        let refreshtoken = localStorage.getItem('refresh')
        return this.http.post(`${environment.apiUrl}/refresh-token/`,{refresh:refreshtoken}).pipe(
            tap(async(res:any) => {
                let user = JSON.parse(localStorage.getItem('currentUser'))
                user.token = res.access_token;
                localStorage.setItem('currentUser', JSON.stringify(user));
                this.authState.next(user);
            })
        )
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        this.authState.next(null);
    }
}