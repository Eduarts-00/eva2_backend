"""
Serializadores de la aplicación inventory.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from rest_framework import serializers
from .models import Categoria, Insumo

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Insumo
        fields = '__all__'
