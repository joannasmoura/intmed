import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '../../../environments/environment';
import { Agenda } from '../models/agenda';
import { Consulta } from '../models/consulta';
import { Especialidade } from '../models/especialidade';
import { Medico } from '../models/medico';
import { Data } from '../models/data';

@Injectable({ providedIn: 'root' })
export class ConsultaService {
    constructor(private http: HttpClient) { }

    getAll() {
        return this.http.get<Consulta[]>(`${environment.apiUrl}/consultas`);
    }

    getEspecialidades(){
        return this.http.get<Especialidade[]>(`${environment.apiUrl}/especialidades`);
    }

    getMedicos(espec){
        return this.http.get<Medico[]>(`${environment.apiUrl}/medicos?especialidade=${espec}`);
    }

    getAgendas(medico){
        return this.http.get<Agenda[]>(`${environment.apiUrl}/agendas?medico=${medico}`);
    }

    marcarConsulta(agenda){
        return this.http.post<Data>(`${environment.apiUrl}/consultas/`, {agenda_id:agenda.data, horario:agenda.hora});
    }
}