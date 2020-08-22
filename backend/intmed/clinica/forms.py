from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Agenda
timeNow = timezone.localtime(timezone.now()) 

class AgendaAdminForm(forms.ModelForm):
    def clean(self): 
        agenda = Agenda.objects.get(medico=self.cleaned_data['medico'],dia=self.cleaned_data['dia'])
        if self.cleaned_data['dia'] < timeNow.today().date():
            raise ValidationError("Não pode criar agenda para um dia passado!")
        if agenda:
            raise ValidationError("Já existe uma agenda para esse médico no dia selecionado!")
