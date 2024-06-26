from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from decouple import config
from product.models import Product
from authentication.models import Customer

from django.utils.html import strip_tags


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)

    SHIPPING_STATUS_CHOICES = (
        ("Pendiente", "Pendiente"),
        ("Enviado", "Enviado"),
        ("Entregado", "Entregado"),
    )

    shipping_status = models.CharField(
        max_length=20, choices=SHIPPING_STATUS_CHOICES, default="Pendiente"
    )

    SHIPPING_METHOD_CHOICES = (
        ("Entrega estándar", "Entrega estándar"),
        ("Recogida en tienda", "Recogida en tienda"),
    )
    shipping_method = models.CharField(
        max_length=25, choices=SHIPPING_METHOD_CHOICES, default="Entrega estándar"
    )

    PAYMENT_METHOD_CHOICES = (
        ("Tarjeta", "Tarjeta"),
        ("Contra-reembolso", "Contra-reembolso"),
    )

    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default="Tarjeta"
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def send_confirmation_email(self):
        subject = "Panadería Sánchez - Confirmación de pedido"
        html_message = render_to_string(
            "order/order_confirmation_email.html", {"order": self}
        )
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(
            subject, plain_message, config("EMAIL_HOST_USER"), [self.customer.user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity
