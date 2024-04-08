from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "price", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()
    shipping_status_choices = serializers.SerializerMethodField(read_only=True)
    payment_method_choices = serializers.SerializerMethodField(read_only=True)
    shipping_method_choices = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "shipping_method",
            "payment_method",
            "created",
            "updated",
            "items",
            "customer",
            "shipping_status",
            "paid",
            "total_cost",
            "shipping_status_choices",
            "payment_method_choices",
            "shipping_method_choices",
        ]
    
    def get_total_cost(self, obj):
        return obj.get_total_cost()
    
    def get_shipping_status_choices(self, obj):
        return dict(Order.SHIPPING_STATUS_CHOICES)
    
    def get_payment_method_choices(self, obj):
        return dict(Order.PAYMENT_METHOD_CHOICES)
    
    def get_shipping_method_choices(self, obj):
        return dict(Order.SHIPPING_METHOD_CHOICES)