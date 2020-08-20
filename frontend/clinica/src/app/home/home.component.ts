import { Component, OnInit } from '@angular/core';
import { User } from '../core/models/user';
import { first } from 'rxjs/operators';
import { ConsultaService  } from '../core/services/consulta.service';
import { Consulta } from '../core/models/consulta';
import {MatDialog, MatDialogConfig} from "@angular/material/dialog";
import { ModalConsultaComponent } from '../modal-consulta/modal-consulta.component';

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
      console.log(consultas)
        this.consultas = consultas;
    });    
  }

  desmarcar(){
    console.log('oi')
  }

  openDialog() {

    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;

    this.dialog.open(ModalConsultaComponent, dialogConfig);
  }
}
