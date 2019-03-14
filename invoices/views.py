from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoicesViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
