"""
Modelos de la aplicación inventory.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from django.db import models

class Categoria(models.Model):
    """
    Clasificación de insumos médicos (Ej: Material Quirúrgico, Medicamentos).
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Campo para borrado lógico (activar/desactivar)")

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    """
    Representa un fármaco o insumo médico disponible en stock.
    """
    categoria = models.ForeignKey(Categoria, related_name='insumos', on_delete=models.CASCADE)
    nombre_comercial = models.CharField(max_length=150)
    principio_activo = models.CharField(max_length=150)
    lote = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    precio_caja = models.DecimalField(max_digits=10, decimal_places=2)
    stock_bodega = models.PositiveIntegerField(default=0, help_text="Cantidad física en bodega")
    is_active = models.BooleanField(default=True, help_text="Campo para borrado lógico (activar/desactivar)")

    def __str__(self):
        return f"{self.nombre_comercial} (Stock: {self.stock_bodega})"
