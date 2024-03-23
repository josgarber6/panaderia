from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "price", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_cost = serializers.SerializerMethodField()
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
            "total_cost"
        ]
    
    def get_total_cost(self, obj):
        return obj.get_total_cost()