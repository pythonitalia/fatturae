from rest_framework import viewsets

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoicesViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
