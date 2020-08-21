from django.urls import path
from django.conf.urls import url
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns=[
    path('', views.index, name='index'),  
    path('registrar/', views.UserCreate.as_view()),
    url(r'^medicos/$', views.MedicoList.as_view(), name='medico-list'),
    url(r'^especialidades/$', views.EspecialidadeList.as_view(), name='especialidade-list'),
    url(r'^agendas/$', views.AgendaList.as_view(), name='agenda-list'),
    url(r'^consultas/$', views.ConsultaList.as_view(), name='consulta-list'),
    path('consultas/<int:pk>/', views.ConsultaList.as_view()),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]