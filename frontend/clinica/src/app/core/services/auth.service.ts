import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, from } from 'rxjs';
import { map,tap } from 'rxjs/operators';
import { JwtHelperService } from "@auth0/angular-jwt";
import { environment } from '../../../environments/environment';
import { User } from '../models/user';
import { AuthResponse } from '../models/auth-response';

const helper = new JwtHelperService();
@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private currentUserSubject: BehaviorSubject<User>;
    public currentUser: Observable<User>;

    constructor(private http: HttpClient) {
        this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
        this.currentUser = this.currentUserSubject.asObservable();
    }    

    public get currentUserValue(): User {
        return this.currentUserSubject.value;
    }

    login(data:User): Observable<AuthResponse> {
        return this.http.post(`${environment.apiUrl}/login/`, data).pipe(
            tap(async (res: AuthResponse) => {
                if (res.access) {
                    let payload = helper.decodeToken(res.access)
                    let user = {
                        username:payload.username, 
                        firstName:payload.firstName, 
                        id:payload.id, 
                        token:res.access,
                        refreshToken: res.refresh,
                        lembrarSenha:data.lembrarSenha} 
                    localStorage.setItem('currentUser', JSON.stringify(user));
                    this.currentUserSubject.next(user);
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
                })
            );
    }

    refreshToken() {
        const refreshToken = this.currentUserValue.refreshToken
        return this.http.post<any>(`${environment.apiUrl}/refresh-token/`, { 'refresh': refreshToken })
            .pipe(
                map(response => {
                    let currentUser: User;
                    if (response.access) {
                        currentUser = helper.decodeToken(response.access)
                        currentUser.token = response.access
                        currentUser.refreshToken = response.refresh
                        currentUser.lembrarSenha = true;
                        localStorage.setItem('currentUser', JSON.stringify(currentUser));
                        this.currentUserSubject.next(currentUser);
                    } 
                    return currentUser;
                }),
            )
    }


    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        this.currentUserSubject.next(null);
    }
}