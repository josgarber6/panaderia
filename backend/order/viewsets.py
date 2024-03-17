from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from product.models import Product
from .serializer import OrderSerializer, OrderItemSerializer
from decimal import Decimal
from two_factor.views.mixins import OTPRequiredMixin
import stripe
from decouple import config

class OrderViewSet(OTPRequiredMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Debe iniciar sesión para realizar un pedido."}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        order = Order.objects.create(
            shipping_method=data["shipping_method"],
            payment_method=data["payment_method"]
        )
        for item in data["items"]:
            product = Product.objects.get(pk=item["product"]["id"])
            OrderItem.objects.create(
                product=product,
                price=item["product"]["price"],
                quantity=item["quantity"],
                order=order
            )
    
        success_url = config("FRONTEND_BASE_URL") + "orders/payment/success"
        cancel_url = config("FRONTEND_BASE_URL") + "orders/payment/cancel"

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

        return Response({"message": "Pedido realizado", "session_url": session.url}, status=status.HTTP_201_CREATED)

class OrderItemViewSet(OTPRequiredMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer