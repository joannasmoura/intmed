import { Medico } from "./medico";

export class Consulta{
    id: number;
    dia: Date;
    horario:Date;
    dataAgendamento:Date;
    medico:Medico;
}