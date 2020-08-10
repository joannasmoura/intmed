from django.contrib import admin
from .models import Especialidade,Medico,Agenda,HorarioAgenda,Consulta

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome','especialidade','crm')

class HorarioAgendaInline(admin.TabularInline):
    exclude = ('disponivel',)
    model = HorarioAgenda
    extra = 1
    verbose_name = "Horário"
    verbose_name_plural = "Horários"    

class AgendaAdmin(admin.ModelAdmin):
    inlines = (HorarioAgendaInline,)
    Agenda.horarios.through.__str__ = lambda x: 'Hora'

admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Especialidade)
admin.site.register(Consulta)
admin.site.register(Medico,MedicoAdmin)