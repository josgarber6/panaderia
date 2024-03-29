from decimal import Decimal

import stripe
from authentication.models import Customer
from decouple import config
from django.conf import settings
from product.models import Product
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from two_factor.views.mixins import OTPRequiredMixin

from .models import Order, OrderItem
from .serializer import OrderItemSerializer, OrderSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

class OrderViewSet(OTPRequiredMixin, viewsets.ModelViewSet):
    # Solo los usuarios autenticados pueden acceder a esta vista
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        if not request.user.is_authenticated and not customer.is_two_factor_enabled():
            return Response({"detail": "Debe iniciar sesión y activar el doble factor de autenticación para realizar un pedido."}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        order = Order.objects.create(
            shipping_method=data["shipping_method"],
            payment_method=data["payment_method"],
            customer=Customer.objects.get(user=request.user)
        )

        if order.payment_method == "Tarjeta":
            order.shipping_status = "Pendiente"
            order.save()

            # Crear los items del pedido y su cantidad correspondiente
            for item in data["items"]:
                product = Product.objects.get(pk=item["product"]["id"])
                OrderItem.objects.create(
                    product=product,
                    price=item["product"]["price"],
                    quantity=item["quantity"],
                    order=order
                )

            # Crear la sesión de pago en Stripe
            success_url = config("FRONTEND_BASE_URL") + "payment/completed"
            cancel_url = config("FRONTEND_BASE_URL") + "payment/cancelled"

            session_data = {
                "mode": "payment",
                "client_reference_id": str(order.id),
                "success_url": success_url,
                "cancel_url": cancel_url,
                "line_items": [],
            }

            for item in order.items.all():
                session_data["line_items"].append(
                    {
                        "price_data": {
                            "unit_amount": int(item.price * Decimal("100")),
                            "currency": "eur",
                            "product_data": {
                                "name": item.product.name,
                            },
                        },
                        "quantity": item.quantity,
                    }
                )

            session = stripe.checkout.Session.create(**session_data)

            return Response({"session_url": session.url, "orderId": order.id}, status=status.HTTP_201_CREATED)
        
        # Si el método de pago es "Contra reembolso"
        else:
            order.shipping_status = "Enviado"
            order.save()

            for item in data["items"]:
                product = Product.objects.get(pk=item["product"]["id"])
                OrderItem.objects.create(
                    product=product,
                    price=item["product"]["price"],
                    quantity=item["quantity"],
                    order=order
                )

            order.send_confirmation_email()
            
            # Devolvemos el pedido y su ID para que el frontend pueda mostrarlo
            return Response({"order": OrderSerializer(order).data, "orderId": order.id}, status=status.HTTP_201_CREATED)
    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            orders = Order.objects.all()
            return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().delete(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    # Endpoint para obtener los pedidos de un usuario
    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def my_orders(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        if not customer.is_two_factor_enabled():
            return Response(status=status.HTTP_403_FORBIDDEN)
        orders = Order.objects.filter(customer=customer)
        return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)
    
class OrderItemViewSet(OTPRequiredMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer