"""
Permisos personalizados para la API.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from rest_framework.permissions import BasePermission

class IsInstitucionMedica(BasePermission):
    """
    Permite acceso únicamente a los usuarios con rol INSTITUCION.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.rol == 'INSTITUCION')

class IsGestorBodega(BasePermission):
    """
    Permite acceso únicamente a los usuarios con rol GESTOR.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.rol == 'GESTOR')
