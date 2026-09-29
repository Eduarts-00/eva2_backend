"""
Serializadores de la aplicación users (Autenticación JWT).
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Personalización del payload del token JWT para incluir el rol del usuario,
    tal como se exige en las especificaciones.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadir claims personalizados
        token['rol'] = user.rol
        token['username'] = user.username

        return token
