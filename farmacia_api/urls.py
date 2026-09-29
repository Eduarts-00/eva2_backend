"""
URLs principales del proyecto farmacia_api.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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
    
    # Documentación Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Catch-all: Redirección global de errores 404 (cualquier ruta extraña va al inicio)
    re_path(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='redirect-404'),
]
