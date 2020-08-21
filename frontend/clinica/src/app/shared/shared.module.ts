import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonComponent } from './components/button/button.component';
import { ModalMessageComponent } from './modal-message/modal-message.component';



@NgModule({
  declarations: [ButtonComponent, ModalMessageComponent],
  imports: [
    CommonModule
  ]
})
export class SharedModule { }
