from django.shortcuts import get_object_or_404,render
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse,Http404
from .models import Consulta, Medico, Especialidade, Agenda
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import EspecialidadeSerializer, MedicoSerializer, AgendaSerializer, ConsultaSerializer,UserSerializer
from .filters import MedicoFilter, EspecialidadeFilter, AgendaFilter
from django.contrib.auth.models import User

class UserCreate(generics.CreateAPIView):
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
    queryset = Agenda.objects.all()    
    filter_class = AgendaFilter

class ConsultaList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    def post(self, request, format=None):
        serializer = ConsultaSerializer(data=request.data)
        if serializer.is_valid():            
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    permission_classes = (IsAuthenticated,)
    consultas = Consulta.objects.all()
    context = {'consultas':consultas}    
    return render(request, 'clinica/index.html', context)

def detail(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    return render(request,'clinica/details.html',{'consulta':consulta})

def results(request, medico_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % medico_id)

def vote(request, medico_id):
    return HttpResponse("You're voting on question %s." % medico_id)