import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';
import { ConsultaService  } from '../core/services/consulta.service';
import { Consulta } from '../core/models/consulta';
import {MatDialog, MatDialogConfig} from "@angular/material/dialog";
import { ModalConsultaComponent } from '../modal-consulta/modal-consulta.component';
import { ModalMessageComponent } from '../shared/modal-message/modal-message.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  loading = false;
  consultas: Consulta[];
  displayedColumns: string[] = ['especialidade', 'profissional', 'data', 'hora','acao'];
  novaConsulta = "Nova Consulta";
  primary="primary";

  constructor(private consultaService: ConsultaService, private dialog: MatDialog) { }

  ngOnInit() {
    this.loading = true;
    this.consultaService.getAll().pipe(first()).subscribe(consultas => {
        this.consultas = consultas;
    });    
  }

  desmarcar(consulta){
    this.consultaService.desmarcarConsulta(consulta).subscribe(
      data =>{
        this.abrirModalDesmarcarErro("Consulta desmarcada com sucesso!");
        this.consultaService.getAll().pipe(first()).subscribe(consultas => {
          this.consultas = consultas;
        });  
      }, 
      err =>{
        this.abrirModalDesmarcarErro(err.error.detail)
      }
    );
  }

  abrirModalMarcarConsulta() {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    this.dialog.open(ModalConsultaComponent, dialogConfig);
  }

  abrirModalDesmarcarErro(message) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = {message:message}
    this.dialog.open(ModalMessageComponent, dialogConfig);
  }
}
