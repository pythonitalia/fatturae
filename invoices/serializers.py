from rest_framework import serializers

from .models import Invoice, Address, Sender


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    recipient_address = AddressSerializer()

    class Meta:
        model = Invoice
        fields = [
            "invoice_number",
            "invoice_type",
            "invoice_currency",
            "invoice_date",
            "invoice_deadline",
            "invoice_tax_rate",
            "invoice_amount",
            "invoice_tax_amount",
            "transmission_format",
            "causal",
            "recipient_tax_code",
            "recipient_last_name",
            "recipient_code",
            "recipient_pec",
            "recipient_address",
        ]

    def create(self, validated_data):
        sender = Sender.objects.get_for_user(self.context["request"].user)

        recipient_address, _ = Address.objects.get_or_create(
            **validated_data["recipient_address"]
        )

        validated_data["recipient_address"] = recipient_address
        validated_data["sender"] = sender

        return Invoice.objects.create(**validated_data)
