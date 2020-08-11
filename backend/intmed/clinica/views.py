from django.shortcuts import get_object_or_404,render
from django.db.models import Q
from django.http import HttpResponse,Http404
from .models import Consulta, Medico, Especialidade, Agenda
from rest_framework import generics
from .serializers import EspecialidadeSerializer, MedicoSerializer, AgendaSerializer, ConsultaSerializer
from .filters import MedicoFilter, EspecialidadeFilter, AgendaFilter

class MedicoList(generics.ListCreateAPIView):    
    serializer_class = MedicoSerializer
    queryset = Medico.objects.all()
    filter_class = MedicoFilter

class EspecialidadeList(generics.ListCreateAPIView):
    serializer_class = EspecialidadeSerializer    
    queryset = Especialidade.objects.all() 
    filter_class = EspecialidadeFilter

class AgendaList(generics.ListCreateAPIView):
    serializer_class = AgendaSerializer
    queryset = Agenda.objects.all()    
    filter_class = AgendaFilter

class ConsultaList(generics.ListCreateAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

def index(request):
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