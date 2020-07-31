from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Especialidade(models.Model):
    nome = models.CharField(max_length=255, default='')
    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=255, default='')
    crm = models.IntegerField(default='')
    email = models.EmailField(blank=True)
    telefone = PhoneNumberField(blank=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nome

class Horario(models.Model):
    hora = models.TimeField(default=timezone.now)
    def __str__(self):
        return str(self.hora)

class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, null=True)
    dia = models.DateField(default=timezone.now)
    horarios = models.ManyToManyField(Horario, through='HorarioAgenda')    
    class Meta:
        unique_together = ('medico', 'dia',)
        constraints = [models.CheckConstraint(check=models.Q(dia__gte=timezone.now()), name='dia_lte'),]
    def __str__(self):
        return self.medico.nome
    

class HorarioAgenda(models.Model):
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)