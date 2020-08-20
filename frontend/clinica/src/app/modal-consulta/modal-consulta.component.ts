import { Component, OnInit } from '@angular/core';
import {MatDialogRef} from '@angular/material/dialog';
import { ConsultaService } from '../core/services/consulta.service';
import { Especialidade } from '../core/models/especialidade';
import { first } from 'rxjs/operators';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Medico } from '../core/models/medico';
import { Agenda } from '../core/models/agenda';
import { Data } from '../core/models/data';
@Component({
  selector: 'app-modal-consulta',
  templateUrl: './modal-consulta.component.html',
  styleUrls: ['./modal-consulta.component.scss']
})
export class ModalConsultaComponent implements OnInit {
  especialidades:Especialidade[];
  medicos:Medico[] = [];
  agendas:Agenda[];
  datas:Data[] = [];
  horarios:Data[] = [];
  labelConfirmar="Confirmar"
  labelCancelar="Cancelar"
  primary="primary";
  secondary="secondary";
  disabledMedico:boolean=true;
  disabledData:boolean=true;
  disabledHora:boolean=true;
  buttonDisabled:boolean=true;
  consultaForm:FormGroup;
  constructor(private formBuilder: FormBuilder, private consultaService:ConsultaService,public dialogRef: MatDialogRef<ModalConsultaComponent>,) { }

  ngOnInit(): void {
    this.consultaForm = this.formBuilder.group({
      especialidade: [''],
      medico: [''],
      data: [''],
      hora:['']
  });
    this.consultaService.getEspecialidades().pipe(first()).subscribe(especialidades => {
        this.especialidades = especialidades;
    });    
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  limpaCamposForm(campos){
    campos.map(c=>{
      this.consultaForm.controls[c].setValue('');
    })
  }

  selectEspecialidade(espec){
    this.consultaService.getMedicos(espec.target.value).pipe(first()).subscribe(medicos => {
      this.medicos = medicos;
      this.limpaCamposForm(['medico','hora','data']);
      this.disabledMedico = false;
      this.disabledData = true;
      this.disabledHora = true;
    })
  }

  selectMedico(medico){
    this.consultaService.getAgendas(medico.target.value).pipe(first()).subscribe(agendas => {      
      this.agendas = agendas;
      this.datas = [];
      agendas.map(a =>{
        this.datas.push({agenda:a.id, data:a.dia})
      })
      this.limpaCamposForm(['hora','data']);
      this.disabledData = false;      
    })
  }

  selectData(agenda){
    let agendaId = agenda.target.value;
    this.horarios = [];
    this.agendas.find(a => a.id == agenda.target.value).horarios.map( a =>{
      this.horarios.push({agenda:agendaId, data:a})
    })
    this.limpaCamposForm(['hora']);
    this.disabledHora = false;
    this.buttonDisabled = false;
  }

  confirmarConsulta(){
    this.consultaService.marcarConsulta(this.consultaForm.value).subscribe(retorno =>{
      console.log(retorno)
    })
  }
}
