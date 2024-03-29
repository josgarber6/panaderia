from rest_framework import viewsets
from .models import Customer
from .serializer import CustomerSerializer
from two_factor.views.mixins import OTPRequiredMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CustomerViewSet(OTPRequiredMixin, viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer