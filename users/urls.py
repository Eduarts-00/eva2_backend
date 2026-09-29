"""
Rutas de autenticación JWT.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada que utiliza el serializador con los claims de rol.
    """
    serializer_class = CustomTokenObtainPairSerializer

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
