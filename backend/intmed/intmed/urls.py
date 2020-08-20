from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinica.urls')),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
