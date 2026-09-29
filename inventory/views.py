"""
Vistas de la aplicación inventory.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Insumo
from .serializers import CategoriaSerializer, InsumoSerializer
from users.permissions import IsGestorBodega

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gestionar categorías.
    GET: Público.
    POST/PUT/DELETE: Solo Gestor de Bodega.
    """
    queryset = Categoria.objects.filter(is_active=True)
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsGestorBodega()]

    def destroy(self, request, *args, **kwargs):
        """Borrado lógico: en lugar de eliminar, desactiva la categoría."""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InsumoFilter(django_filters.FilterSet):
    """Filtros personalizados para el catálogo de insumos."""
    min_precio = django_filters.NumberFilter(field_name="precio_caja", lookup_expr='gte', help_text="Precio mínimo")
    max_precio = django_filters.NumberFilter(field_name="precio_caja", lookup_expr='lte', help_text="Precio máximo")

    class Meta:
        model = Insumo
        fields = ['categoria', 'principio_activo']

class InsumoViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gestionar el catálogo de insumos.
    GET: Público. Se aplican filtros usando django-filter.
    POST/PUT/DELETE: Solo Gestor de Bodega.
    """
    queryset = Insumo.objects.filter(is_active=True)
    serializer_class = InsumoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InsumoFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsGestorBodega()]

    def destroy(self, request, *args, **kwargs):
        """Borrado lógico: en lugar de eliminar, desactiva el insumo."""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
