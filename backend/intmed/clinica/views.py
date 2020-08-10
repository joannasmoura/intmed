from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,Http404
from .models import Consulta, Medico, Especialidade, Agenda
from rest_framework import generics
from .serializers import EspecialidadeSerializer, MedicoSerializer, AgendaSerializer, ConsultaSerializer

class MedicoList(generics.ListCreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class EspecialidadeList(generics.ListCreateAPIView):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer

class AgendaList(generics.ListCreateAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

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