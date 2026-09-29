"""
Rutas de la aplicación orders.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarroInsumosViewSet, CheckoutView, MisSolicitudesViewSet, SolicitudGestorViewSet

router = DefaultRouter()
router.register(r'carro-insumos', CarroInsumosViewSet, basename='carro')
router.register(r'mis-solicitudes', MisSolicitudesViewSet, basename='mis-solicitudes')
router.register(r'solicitudes', SolicitudGestorViewSet, basename='solicitudes-gestor')

urlpatterns = [
    path('', include(router.urls)),
    path('solicitudes/confirmar/', CheckoutView.as_view(), name='checkout'),
]
