from django.contrib import admin
from .models import Categoria, Insumo

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'is_active')
    search_fields = ('nombre',)

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'categoria', 'precio_caja', 'stock_bodega', 'is_active')
    list_filter = ('categoria', 'is_active')
    search_fields = ('nombre_comercial', 'principio_activo', 'lote')
