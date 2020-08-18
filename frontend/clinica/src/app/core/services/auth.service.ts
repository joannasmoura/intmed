import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map,tap } from 'rxjs/operators';

import { environment } from '../../../environments/environment';
import { User } from '../models/user';
import { AuthResponse } from '../models/auth-response';

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
                    if (res.token) {
                        user.token = res.token
                        localStorage.setItem('currentUser', JSON.stringify(user));
                        this.authState.next(user);
                        return user;
                    }
                })
            );
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        this.authState.next(null);
    }
}