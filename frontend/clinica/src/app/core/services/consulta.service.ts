import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '../../../environments/environment';
import { Agenda } from '../models/agenda';
import { Consulta } from '../models/consulta';

@Injectable({ providedIn: 'root' })
export class ConsultaService {
    constructor(private http: HttpClient) { }

    getAll() {
        return this.http.get<Consulta[]>(`${environment.apiUrl}/consultas`);
    }
}