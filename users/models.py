"""
Modelos de la aplicación de usuarios.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que incluye el rol del usuario,
    fundamental para el control de acceso basado en roles (RBAC).
    """
    class Roles(models.TextChoices):
        INSTITUCION = 'INSTITUCION', 'Institución Médica'
        GESTOR = 'GESTOR', 'Gestor de Bodega Farmacéutica'

    rol = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.INSTITUCION,
        help_text='Rol del usuario en la plataforma B2B'
    )

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
