from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "paid",
        "shipping_status",
        "shipping_method",
        "payment_method",
        "created",
        "updated",
    ]
    inlines = [OrderItemInline]


# @admin.register(Claim)
# class ClaimAdmin(admin.ModelAdmin):
#     list_display = ["order", "comment", "creation_date"]
