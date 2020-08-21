import { Component, OnInit, Inject } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-modal-message',
  templateUrl: './modal-message.component.html',
  styleUrls: ['./modal-message.component.scss']
})
export class ModalMessageComponent implements OnInit {
  labelConfirmar="Ok"
  primary="primary";
  constructor(
    public dialogRef: MatDialogRef<ModalMessageComponent>, 
    @Inject(MAT_DIALOG_DATA) public data: {message:string}
  ) { }

  ngOnInit(): void {
  }

  onOkClick(): void {
    this.dialogRef.close();
  }

}
