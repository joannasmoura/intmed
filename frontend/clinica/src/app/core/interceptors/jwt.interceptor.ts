import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { catchError, switchMap, filter, take} from 'rxjs/operators';

import { AuthenticationService } from '../services/auth.service';
import { environment } from 'src/environments/environment';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
    constructor(private authenticationService: AuthenticationService) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const currentUser = this.authenticationService.currentUserValue;
        const isLoggedIn = currentUser && currentUser.token;
        const isApiUrl = request.url.startsWith(environment.apiUrl);

        if (isLoggedIn 
            && isApiUrl 
            && currentUser 
            && request.url != `${environment.apiUrl}/refresh-token/` 
            && request.url != `${environment.apiUrl}/login/` 
            ) {
            request = request.clone({
                setHeaders: {
                    Authorization: `Token ${currentUser.token}`
                }
            });
        } 

        return next.handle(request).pipe(catchError(err => {
          const lembrarSenha = currentUser ? currentUser.lembrarSenha : false
            if ( err instanceof HttpErrorResponse && ((err.status === 401 || err.status === 403) && request.url === `${environment.apiUrl}/refresh-token/`) || (!lembrarSenha && request.url !== `${environment.apiUrl}/registrar/`)) {
              this.authenticationService.logout();
              location.reload()
              return throwError(err);
            }else if (err instanceof HttpErrorResponse && err.status === 401) {
                return this.handle401Error(request, next);
            } else {
                return throwError(err);
            }
        }));
    }

    private isRefreshing = false;
    private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

    private handle401Error(request: HttpRequest<any>, next: HttpHandler) {
        // console.log('handling 403')
        if (!this.isRefreshing) {
          this.isRefreshing = true;
          this.refreshTokenSubject.next(null);

          return this.authenticationService.refreshToken().pipe(
            switchMap((token: any) => {
              this.isRefreshing = false;
              this.refreshTokenSubject.next(token.jwt);
              return next.handle(this.addToken(request, token.jwt));
            }));
      
        } else {
          return this.refreshTokenSubject.pipe(
            filter(token => token != null),
            take(1),
            switchMap(jwt => {
              return next.handle(this.addToken(request, jwt));
            }));
        }
      }

    private addToken(request: HttpRequest<any>, token: string) {
        const currentUser = this.authenticationService.currentUserValue;
        return request.clone({
          setHeaders: {
            'Authorization': `Token  ${currentUser.token}`
          }
        });
      }
}