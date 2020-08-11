from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinica.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', obtain_jwt_token),
    url(r'^refresh-token/', refresh_jwt_token),
]
