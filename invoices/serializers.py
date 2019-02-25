from rest_framework import serializers

from .models import Invoice, Address, Sender, Item


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["description", "quantity", "unit_price", "vat_rate"]


class InvoiceSerializer(serializers.ModelSerializer):
    recipient_address = AddressSerializer()
    items = ItemSerializer(many=True)

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
            "items",
            "recipient_tax_code",
            "recipient_denomination",
            "recipient_first_name",
            "recipient_last_name",
            "recipient_code",
            "recipient_pec",
            "recipient_address",
        ]

    # TODO: atomic
    def create(self, validated_data):
        sender = Sender.objects.get_for_user(self.context["request"].user)

        recipient_address, _ = Address.objects.get_or_create(
            **validated_data["recipient_address"]
        )

        validated_data["recipient_address"] = recipient_address
        validated_data["sender"] = sender

        items = validated_data.pop("items", [])

        invoice = Invoice.objects.create(**validated_data)

        for index, item in enumerate(items):
            Item.objects.create(row=index + 1, invoice=invoice, **item)

        return invoice

    def validate(self, data):
        denomination = data.get("recipient_denomination")
        first_name = data.get("recipient_first_name")
        last_name = data.get("recipient_last_name")

        if not denomination and not all([first_name, last_name]):
            raise serializers.ValidationError(
                "You need to specify either recipient_denomination or "
                "both recipient_first_name and recipient_last_name"
            )

        return data
