from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Especialidade(models.Model):
    nome = models.CharField(max_length=255, default='')
    class Meta:
         db_table = "especialidade"
    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=255, default='')
    crm = models.IntegerField(default='')
    email = models.EmailField(blank=True)
    telefone = PhoneNumberField(blank=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE, null=True)
    class Meta:
         db_table = "medico"
    def __str__(self):
        return self.nome

class Horario(models.Model):
    hora = models.TimeField(default=timezone.now)
    class Meta:
         db_table = "horario"
    def __str__(self):
        return str(self.hora)

class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, null=True)
    dia = models.DateField(default=timezone.now)
    horarios = models.ManyToManyField(Horario, through='HorarioAgenda')
    class Meta:
         db_table = "agenda"        
    def __str__(self):
        return self.medico.nome + ' - ' + self.dia.strftime("%d/%m/%Y")
    

class HorarioAgenda(models.Model):
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)
    class Meta:
         db_table = "horario_agenda"

class Consulta(models.Model):    
    horario_agenda = models.ForeignKey(HorarioAgenda, on_delete=models.CASCADE, null=True)
    data_agendamento = models.DateTimeField(default=timezone.now)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, null=True)
    class Meta:
         db_table = "consulta"
    def __str__(self):
        return self.medico.nome + ' - ' + self.horario_agenda.agenda.dia.strftime("%d/%m/%Y") + ' - ' + self.horario_agenda.horario.hora.strftime("%H:%M")