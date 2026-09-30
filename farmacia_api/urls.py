"""
URLs principales del proyecto farmacia_api.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from django.shortcuts import render

def custom_404_view(request, exception=None):
    return render(request, '404_custom.html', status=404)

urlpatterns = [
    # Vista HTML Base (Portal de Inicio)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # Panel de administración
    path('admin/', admin.site.urls),
    
    # Rutas de autenticación JWT
    path('api/auth/', include('users.urls')),
    
    # Rutas de inventario y órdenes
    path('api/', include('inventory.urls')),
    path('api/', include('orders.urls')),
    
    # Documentación Swagger / OpenAPI / Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Catch-all: Página de error 404 bonita
    re_path(r'^.*$', custom_404_view, name='error-404'),
]
