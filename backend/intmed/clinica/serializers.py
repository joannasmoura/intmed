from rest_framework import serializers
from clinica.models import Medico, Especialidade, Agenda,Horario, HorarioAgenda,Consulta
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils import timezone
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework.fields import CurrentUserDefault
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    class Meta:
        model = User
        fields = ['username','first_name','email','password']
        extra_kwargs = {'password': {'write_only': True}}

class EspecialidadeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(required=True, max_length=100)  
    class Meta:
        model = Especialidade
        fields = '__all__'    
    
class MedicoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    crm = serializers.CharField(required=True)
    nome = serializers.CharField(required=True, max_length=100)    
    especialidade = EspecialidadeSerializer()
    class Meta:
        model = Medico
        fields = ('id', 'crm', 'nome', 'especialidade') 

class HorarioSerializer(serializers.ModelSerializer):
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

class AgendaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    medico = MedicoSerializer()
    dia = serializers.DateField()    
    horarios = serializers.SerializerMethodField()
    def get_horarios(self, agenda):
        return agenda.horarios.values_list('hora', flat=True)
    class Meta:
        model = Agenda
        fields = ('id', 'medico', 'dia','horarios')

class ConsultaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)        
    dia  = serializers.ReadOnlyField(source='horario_agenda.agenda.dia', read_only=True)
    horario = serializers.TimeField(source='horario_agenda.horario.hora',label='horario')
    data_agendamento = serializers.DateTimeField(default=timezone.now)
    medico = MedicoSerializer(source='horario_agenda.agenda.medico',required=False, read_only=True)
    horario_agenda = HorarioAgendaSerializer(write_only=True,required=False)
    agenda_id = serializers.IntegerField(write_only=True)
    owner = UserSerializer(default=serializers.CurrentUserDefault())
    def create(self, data):
        user = User.objects.get(username=self.context['request'].user)
        horario = data['horario_agenda']['horario']['hora']
        agenda_id = data['agenda_id']
        ha = HorarioAgenda.objects.get(agenda__id=agenda_id,horario__hora=str(horario))
        ha.disponivel = False
        ha.save()
        c = Consulta(data_agendamento=data['data_agendamento'], horario_agenda=ha,owner=user)
        c.save() 
        return c
    class Meta:
        model = Consulta
        fields = ('id', 'dia', 'horario', 'data_agendamento', 'medico','agenda_id','horario_agenda','owner')