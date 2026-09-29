"""
Modelos de la aplicación orders.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from django.db import models
from django.conf import settings
from inventory.models import Insumo

class Carro(models.Model):
    """
    Carro de compras B2B persistente.
    Relación 1 a 1 con el usuario (Institución Médica).
    Mantiene los ítems aunque el usuario cierre sesión.
    """
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carro')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carro de {self.usuario.username}"

class CarroItem(models.Model):
    """
    Ítem individual dentro del carro de compras.
    """
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='items')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carro', 'insumo') # Evitar duplicados del mismo insumo

    def __str__(self):
        return f"{self.cantidad}x {self.insumo.nombre_comercial}"

class Solicitud(models.Model):
    """
    Orden de compra generada tras el checkout.
    """
    class Estados(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADO = 'PAGADO', 'Pagado'
        ENTREGADO = 'ENTREGADO', 'Entregado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    institucion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes')
    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.PENDIENTE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Solicitud {self.id} - {self.get_estado_display()}"

class SolicitudItem(models.Model):
    """
    Detalle inmutable de los ítems adquiridos en una solicitud.
    """
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='detalles')
    insumo = models.ForeignKey(Insumo, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.insumo.nombre_comercial if self.insumo else 'Insumo Eliminado'} (Sol: {self.solicitud.id})"
