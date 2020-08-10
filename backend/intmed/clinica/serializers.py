from rest_framework import serializers
from clinica.models import Medico, Especialidade, Agenda,Horario, HorarioAgenda,Consulta
from phonenumber_field.serializerfields import PhoneNumberField

class EspecialidadeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(required=True, max_length=100)  
    class Meta:
        model = Especialidade
        fields = '__all__'
    
class MedicoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    crm = serializers.CharField(required=True)
    nome = serializers.CharField(required=True, max_length=100)    
    especialidade = EspecialidadeSerializer()
    class Meta:
        model = Medico
        fields = '__all__'

class HorarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    hora = serializers.TimeField()    
    class Meta:
        model = Horario
        fields = '__all__'

class HorarioAgendaSerializer(serializers.HyperlinkedModelSerializer):    
    hora = serializers.ReadOnlyField(source='horario.hora')
    dia = serializers.ReadOnlyField(source='agenda.dia')
    class Meta:
        model = HorarioAgenda
        fields = ('hora','dia',)

class AgendaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    medico = MedicoSerializer()
    dia = serializers.DateField()    
    horarios = serializers.SerializerMethodField()
    def get_horarios(self, agenda):
        return agenda.horarios.values_list('hora', flat=True)
    class Meta:
        model = Agenda
        fields = ('id', 'medico', 'dia','horarios')

class ConsultaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    dia=serializers.DateField(read_only=True, source='horario_agenda.agenda.dia')
    horario= serializers.TimeField(read_only=True, source='horario_agenda.horario.hora')
    data_agendamento = serializers.DateTimeField()
    medico = MedicoSerializer()        
    class Meta:
        model = Consulta
        fields = ('id','dia','horario', 'data_agendamento','medico')