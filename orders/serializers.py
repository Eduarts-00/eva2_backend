"""
Serializadores de la aplicación orders.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from rest_framework import serializers
from .models import Carro, CarroItem, Solicitud, SolicitudItem
from inventory.serializers import InsumoSerializer

class CarroItemSerializer(serializers.ModelSerializer):
    insumo_detalle = InsumoSerializer(source='insumo', read_only=True)

    class Meta:
        model = CarroItem
        fields = ['id', 'insumo', 'insumo_detalle', 'cantidad']

class CarroSerializer(serializers.ModelSerializer):
    items = CarroItemSerializer(many=True, read_only=True)

    class Meta:
        model = Carro
        fields = ['id', 'usuario', 'creado_en', 'items']

class SolicitudItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudItem
        fields = ['id', 'insumo', 'cantidad', 'precio_unitario']

class SolicitudSerializer(serializers.ModelSerializer):
    detalles = SolicitudItemSerializer(many=True, read_only=True)

    class Meta:
        model = Solicitud
        fields = ['id', 'institucion', 'estado', 'fecha_creacion', 'total', 'detalles']
        read_only_fields = ['institucion', 'fecha_creacion', 'total']

class SolicitudEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['estado']
