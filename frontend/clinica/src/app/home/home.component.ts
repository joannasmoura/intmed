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
    this.getConsultas();
  }

  getConsultas(){
    this.consultaService.getAll().pipe(first()).subscribe(consultas => {
      this.consultas = consultas;
    }); 
  }

  desmarcar(consulta){
    this.consultaService.desmarcarConsulta(consulta).subscribe(
      data =>{
        this.abrirModalMensagem("Consulta desmarcada com sucesso!", true);
        this.consultaService.getAll().pipe(first()).subscribe(consultas => {
          this.consultas = consultas;
        });  
      }, 
      err =>{
        this.abrirModalMensagem(err.error.detail, false)
      }
    );
  }

  abrirModalMarcarConsulta() {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    let dialogRef = this.dialog.open(ModalConsultaComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(res =>{
      this.getConsultas()
    })
  }

  abrirModalMensagem(message, success) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = {message:message, success:success}
    let dialogRef = this.dialog.open(ModalMessageComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(res =>{
      this.getConsultas()
    })
  }
}
