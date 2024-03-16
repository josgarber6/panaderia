from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order, OrderItem
from product.models import Product
from .serializer import OrderSerializer, OrderItemSerializer
from django_otp.decorators import otp_required

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # @otp_required
    def create(self, request, *args, **kwargs):
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
        return Response(status=status.HTTP_201_CREATED)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer