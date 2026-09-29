"""
Rutas de la aplicación inventory.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, InsumoViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'insumos', InsumoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
