import datetime
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404,render
from django.db.models import Q
from rest_framework import status,exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse,Http404
from .models import Consulta, Medico, Especialidade, Agenda,User,HorarioAgenda
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import EspecialidadeSerializer, MedicoSerializer, AgendaSerializer, ConsultaSerializer,UserSerializer
from .filters import MedicoFilter, EspecialidadeFilter, AgendaFilter
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
timeNow = timezone.localtime(timezone.now()) 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['firstName'] = user.first_name
        token['username'] = user.username
        token['id'] = user.id
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserCreate(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

class MedicoList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)         
    serializer_class = MedicoSerializer
    queryset = Medico.objects.all()
    filter_class = MedicoFilter

class EspecialidadeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EspecialidadeSerializer    
    queryset = Especialidade.objects.all() 
    filter_class = EspecialidadeFilter

class AgendaList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AgendaSerializer
    queryset = Agenda.objects.all().order_by('dia').exclude(dia__lt=datetime.date.today())
    filter_class = AgendaFilter
    
class ConsultaList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        consultas = Consulta.objects.all().filter(
            owner__id=user.id
        ).order_by(
        'horario_agenda__agenda__dia',
        'horario_agenda__horario__hora'
        ).exclude(
            horario_agenda__agenda__dia__lt=timeNow
        ).exclude(
            horario_agenda__horario__hora__lt=str(timeNow.time())
        )
        return consultas
    def post(self, request, format=None):
        if hasConsultaDiaHorario(request):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"detail":"Você ja possui uma consulta marcada para esse dia e horário."})
        if hasDiaHorarioPassed(request):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"detail":"O dia e o horário que você está tentando marcar a consulta ja passaram."})
        if hasDiaHorarioBeenFilled(request):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"detail":"A data e o horario que você está tentando marcar não estão disponíveis para esse médico!"})
        serializer = ConsultaSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            consulta = self.get_object()
        except Consulta.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)
        if consulta.owner != request.user:        
            return Response(status=status.HTTP_403_FORBIDDEN,data={"detail":"Apenas o usuário que marcou a consulta pode desmarcá-la."})
        if consulta.horario_agenda.agenda.dia < datetime.date.today():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,data={"detail":"Não é possível desmarcar pois a data da consulta ja passou."})
        consulta.delete()
        ha = HorarioAgenda.objects.get(pk=consulta.horario_agenda.id)
        ha.disponivel = True
        ha.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

def index(request):
    permission_classes = (IsAuthenticated,)
    consultas = Consulta.objects.all()
    context = {'consultas':consultas}    
    return render(request, 'clinica/index.html', context)

def hasConsultaDiaHorario(request):
    user = User.objects.get(username=request.user)
    agenda = Agenda.objects.get(pk=request.data['agenda_id'])
    horario = request.data['horario']
    try:    
        consultaExistente = Consulta.objects.get(owner=user,horario_agenda__agenda__dia=agenda.dia,horario_agenda__horario__hora=horario)        
    except:
        return False
    return consultaExistente

def hasDiaHorarioPassed(request):
    try:
        agenda = Agenda.objects.get(pk=request.data['agenda_id'])
    except:
        return False
    dia = datetime.datetime.combine(agenda.dia, datetime.time(0, 0))
    horario = request.data['horario']
    if dia > timeNow.today():
        return True
    elif horario < str(timeNow.time()):
        return True
    else:
        return False

def hasDiaHorarioBeenFilled(request):
    agenda = Agenda.objects.get(pk=request.data['agenda_id'])    
    horario = request.data['horario']
    try:    
        consultaExistente = Consulta.objects.get(horario_agenda__agenda__dia=agenda.dia,horario_agenda__horario__hora=horario)
    except:
        return False
    return consultaExistente

# def get(self, request, format=None):
#     user = User.objects.get(username=request.user)
    # queryset = Consulta.objects.all().filter(
    #     owner__id=user.id
    # ).order_by(
    # 'horario_agenda__agenda__dia',
    # 'horario_agenda__horario__hora'
    # ).exclude(
    #     horario_agenda__agenda__dia__lt=timeNow
    # ).exclude(
    #     horario_agenda__horario__hora__lt=str(timeNow.time())
    # )
#     serializer = ConsultaSerializer(queryset)
#     return Response(serializer.data)