from django_filters import FilterSet, NumberFilter, CharFilter, ModelMultipleChoiceFilter, DateFilter, BooleanFilter
from .models import Consulta, Medico, Especialidade,Agenda

class MedicoFilter(FilterSet):
    especialidade = ModelMultipleChoiceFilter(field_name='especialidade__id',to_field_name='id', queryset=Especialidade.objects.all())
    search = CharFilter( lookup_expr='icontains',field_name='nome')
    class Meta:
        model = Medico
        fields = ['especialidade','nome']        


class EspecialidadeFilter(FilterSet):
    search = CharFilter( lookup_expr='icontains',field_name='nome')
    class Meta:
        model = Especialidade
        fields = ['nome']  

class AgendaFilter(FilterSet):
    especialidade = ModelMultipleChoiceFilter(field_name='medico__especialidade__id', to_field_name='id', queryset=Especialidade.objects.all())
    medico = ModelMultipleChoiceFilter(field_name='medico__id', to_field_name='id', queryset=Medico.objects.all())
    data_inicio = DateFilter(field_name='dia',lookup_expr=('gte'),) 
    data_final = DateFilter(field_name='dia',lookup_expr=('lte'))
    horario = BooleanFilter(field_name='horarios__disponivel', lookup_expr=True)
    class Meta:
        model:Agenda
        fields = ['especialidade','medico','dia']