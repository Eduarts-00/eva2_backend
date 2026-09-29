"""
Vistas de la aplicación orders.
Alumno: Edu
Sección: Por defecto
Año: 2026
"""
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Carro, CarroItem, Solicitud, SolicitudItem
from .serializers import CarroSerializer, CarroItemSerializer, SolicitudSerializer, SolicitudEstadoSerializer
from users.permissions import IsInstitucionMedica, IsGestorBodega

class CarroInsumosViewSet(viewsets.ViewSet):
    """
    Gestión del carro de compras persistente.
    Endpoints: GET/POST/DELETE /api/carro-insumos/
    Solo accesible por la Institución Médica.
    """
    permission_classes = [IsInstitucionMedica]

    def list(self, request):
        """Obtiene el carro del usuario actual (lo crea si no existe)"""
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        serializer = CarroSerializer(carro)
        return Response(serializer.data)

    def create(self, request):
        """Agrega un insumo al carro"""
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        insumo_id = request.data.get('insumo')
        cantidad = int(request.data.get('cantidad', 1))

        if not insumo_id:
            return Response({'error': 'Debe proveer un ID de insumo'}, status=status.HTTP_400_BAD_REQUEST)

        # Si el ítem ya está en el carro, sumamos la cantidad
        item, created = CarroItem.objects.get_or_create(carro=carro, insumo_id=insumo_id)
        if not created:
            item.cantidad += cantidad
            item.save()
        else:
            item.cantidad = cantidad
            item.save()

        return Response(CarroSerializer(carro).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """Elimina un ítem específico del carro"""
        carro = get_object_or_404(Carro, usuario=request.user)
        item = get_object_or_404(CarroItem, id=pk, carro=carro)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CheckoutView(views.APIView):
    """
    Endpoint para confirmar el carro y crear la solicitud.
    POST /api/solicitudes/confirmar/
    """
    permission_classes = [IsInstitucionMedica]

    def post(self, request):
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        items = carro.items.all()

        if not items.exists():
            return Response({'error': 'El carro está vacío'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Control transaccional: Bloque atómico
            with transaction.atomic():
                total = 0
                
                # Validación de stock
                for item in items:
                    insumo = item.insumo
                    if insumo.stock_bodega < item.cantidad:
                        raise ValueError(f"Stock insuficiente para {insumo.nombre_comercial}. Solicitado: {item.cantidad}, Disponible: {insumo.stock_bodega}")
                    total += insumo.precio_caja * item.cantidad

                # Crear Solicitud en estado PAGADO (se liquida el stock)
                solicitud = Solicitud.objects.create(
                    institucion=request.user,
                    estado=Solicitud.Estados.PAGADO,
                    total=total
                )

                # Descontar stock y generar histórico
                for item in items:
                    insumo = item.insumo
                    # Descuento físico en bodega
                    insumo.stock_bodega -= item.cantidad
                    insumo.save()

                    SolicitudItem.objects.create(
                        solicitud=solicitud,
                        insumo=insumo,
                        cantidad=item.cantidad,
                        precio_unitario=insumo.precio_caja
                    )

                # Vaciar el carro
                items.delete()

            serializer = SolicitudSerializer(solicitud)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Si falla la validación de stock, la transacción se deshace (rollback)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MisSolicitudesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Historial de compras de la Institución Médica.
    GET /api/mis-solicitudes/
    """
    permission_classes = [IsInstitucionMedica]
    serializer_class = SolicitudSerializer

    def get_queryset(self):
        return Solicitud.objects.filter(institucion=self.request.user).order_by('-fecha_creacion')

class SolicitudGestorViewSet(viewsets.ModelViewSet):
    """
    Gestión de órdenes por parte del Gestor de Bodega.
    PATCH /api/solicitudes/{id}/estado/
    """
    permission_classes = [IsGestorBodega]
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    @action(detail=True, methods=['patch'])
    def estado(self, request, pk=None):
        solicitud = self.get_object()
        serializer = SolicitudEstadoSerializer(solicitud, data=request.data, partial=True)
        
        if serializer.is_valid():
            nuevo_estado = serializer.validated_data.get('estado')
            estado_anterior = solicitud.estado

            with transaction.atomic():
                # Si se cancela una orden que no estaba cancelada previamente
                if nuevo_estado == Solicitud.Estados.CANCELADO and estado_anterior != Solicitud.Estados.CANCELADO:
                    # Reposición de stock
                    for detalle in solicitud.detalles.all():
                        if detalle.insumo:
                            detalle.insumo.stock_bodega += detalle.cantidad
                            detalle.insumo.save()
                
                # Opcional: Manejar el caso de des-cancelar (no requerido pero útil)
                elif estado_anterior == Solicitud.Estados.CANCELADO and nuevo_estado in [Solicitud.Estados.PAGADO, Solicitud.Estados.ENTREGADO]:
                    # Volver a descontar stock
                    for detalle in solicitud.detalles.all():
                        if detalle.insumo:
                            if detalle.insumo.stock_bodega < detalle.cantidad:
                                raise ValueError(f"Stock insuficiente para re-activar {detalle.insumo.nombre_comercial}")
                            detalle.insumo.stock_bodega -= detalle.cantidad
                            detalle.insumo.save()

                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
