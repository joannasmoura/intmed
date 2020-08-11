from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns=[
    path('', views.index, name='index'),  
    path('<int:consulta_id>/', views.detail, name='detail'),    
    path('<int:consulta_id>/results/', views.results, name='results'),    
    path('<int:consulta_id>/vote/', views.vote, name='vote'),
    url(r'^medicos/$', views.MedicoList.as_view(), name='medico-list'),
    url(r'^especialidades/$', views.EspecialidadeList.as_view(), name='especialidade-list'),
    # url(r'^especialidades/(?P<id>.+)/$', views.EspecialidadeList.as_view('retrieve')),
    url(r'^agendas/$', views.AgendaList.as_view(), name='agenda-list'),
    url(r'^consultas/$', views.ConsultaList.as_view(), name='consulta-list'),
]