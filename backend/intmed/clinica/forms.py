from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Agenda
timeNow = timezone.localtime(timezone.now()) 

class AgendaAdminForm(forms.ModelForm):
    id = forms.CharField(widget = forms.HiddenInput(),required=False)
    def clean(self):         
        check = False
        try:
            agenda = Agenda.objects.get(medico=self.cleaned_data['medico'],dia=self.cleaned_data['dia'])
            id = self.cleaned_data['id']
            check = str(agenda.id) != str(id)
        except:
            id = None
            agenda = None        
        
        if self.cleaned_data['dia'] < timeNow.today().date():
            raise ValidationError("Não pode criar agenda para um dia passado!")
        if id != None and check:
            raise ValidationError("Já existe uma agenda para esse médico no dia selecionado!")