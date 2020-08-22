from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Especialidade,Medico,Agenda,HorarioAgenda,User,Horario
from .forms import AgendaAdminForm

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome','especialidade','crm')

class HorarioAgendaInline(admin.TabularInline):
    exclude = ('disponivel',)
    model = HorarioAgenda
    extra = 1
    verbose_name = "Horário"
    verbose_name_plural = "Horários"    


class AgendaAdmin(admin.ModelAdmin):
    form = AgendaAdminForm
    inlines = (HorarioAgendaInline,)

admin.site.register(User, UserAdmin)
admin.site.register(Horario)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Especialidade)
admin.site.register(Medico,MedicoAdmin)