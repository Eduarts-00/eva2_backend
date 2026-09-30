from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer
from django.contrib.auth import get_user_model

class CustomTokenObtainPairView(TokenObtainPairView):
    """Vista personalizada para devolver el token JWT con el rol incluido."""
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    """Endpoint para registrar nuevas Instituciones Médicas (Clientes)."""
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
