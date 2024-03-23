from rest_framework import viewsets
from .models import Customer
from .serializer import CustomerSerializer
from two_factor.views.mixins import OTPRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CustomerViewSet(OTPRequiredMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request):
        if request.user.is_staff:
            queryset = Customer.objects.all()
            serializer = CustomerSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "No tiene permisos para ver esta información."}, status=403)
