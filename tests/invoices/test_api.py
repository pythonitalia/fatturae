from datetime import date, timedelta
from decimal import Decimal

import pytest

from django.urls import reverse

from invoices.models import Invoice


def test_fails_with_empty_data(api_client, user):
    api_client.force_login(user)

    response = api_client.post(reverse("invoice-list"), {}, format="json")

    assert response.status_code == 400


def test_creates_with_users_sender(api_client, user, sender):
    api_client.force_login(user)

    response = api_client.post(
        reverse("invoice-list"),
        {
            "invoice_number": "1234",
            "invoice_currency": "EUR",
            "invoice_tax_amount": 10,
            "transmission_format": "FPA12",
            "recipient_address": {
                "address": "Via Roma",
                "postcode": "50123",
                "city": "Florence",
                "country_code": "IT",
            },
            "invoice_type": "TD01",
            "invoice_tax_rate": 22.0,
            "invoice_date": date.today().isoformat(),
            "invoice_deadline": (
                date.today() + timedelta(days=30)
            ).isoformat(),
            "invoice_amount": 30,
            "recipient_code": "XXXXXXX",
            "items": [
                {
                    "description": "Sample item",
                    "unit_price": 30,
                    "quantity": 1,
                    "vat_rate": 22.0,
                }
            ],
            "recipient_denomination": "Example srl",
            "payment_condition": "TP02",
            "payment_method": "MP08",
        },
        format="json",
    )

    assert response.status_code == 201

    assert Invoice.objects.count() == 1
    invoice = Invoice.objects.first()

    assert invoice.items.count() == 1
    item = invoice.items.first()

    assert item.description == "Sample item"


def test_test_wants_both_first_and_last_name(api_client, user, sender):
    api_client.force_login(user)

    response = api_client.post(
        reverse("invoice-list"),
        {
            "invoice_number": "1234",
            "invoice_currency": "EUR",
            "invoice_tax_amount": 10,
            "transmission_format": "FPA12",
            "recipient_address": {
                "address": "Via Roma",
                "postcode": "50123",
                "city": "Florence",
                "country_code": "IT",
            },
            "invoice_type": "TD01",
            "invoice_tax_rate": 22.0,
            "invoice_date": date.today().isoformat(),
            "invoice_deadline": (
                date.today() + timedelta(days=30)
            ).isoformat(),
            "items": [
                {
                    "description": "Sample item",
                    "unit_price": 30,
                    "quantity": 1,
                    "vat_rate": 22.0,
                }
            ],
            "invoice_amount": 30,
            "recipient_code": "XXXXXXX",
            "recipient_first_name": "Patrick",
            "payment_condition": "TP02",
            "payment_method": "MP08",
        },
        format="json",
    )

    assert response.status_code == 400

    assert response.json() == {
        "non_field_errors": [
            "You need to specify either recipient_denomination or "
            "both recipient_first_name and recipient_last_name"
        ]
    }

    response = api_client.post(
        reverse("invoice-list"),
        {
            "invoice_number": "1234",
            "invoice_currency": "EUR",
            "invoice_tax_amount": 10,
            "transmission_format": "FPA12",
            "recipient_address": {
                "address": "Via Roma",
                "postcode": "50123",
                "city": "Florence",
                "country_code": "IT",
            },
            "invoice_type": "TD01",
            "invoice_tax_rate": 22.0,
            "invoice_date": date.today().isoformat(),
            "invoice_deadline": (
                date.today() + timedelta(days=30)
            ).isoformat(),
            "invoice_amount": 30,
            "items": [
                {
                    "description": "Sample item",
                    "unit_price": 30,
                    "quantity": 1,
                    "vat_rate": 22.0,
                }
            ],
            "recipient_code": "XXXXXXX",
            "recipient_first_name": "Patrick",
            "recipient_last_name": "Arminio",
            "payment_condition": "TP02",
            "payment_method": "MP08",
        },
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.parametrize(
    "code, pec", [(None, "patrick@python.it"), ("XXXXXXX", None)]
)
def test_works_with_either_pec_or_recipient_code(
    api_client, user, sender, code, pec
):
    api_client.force_login(user)

    data = {
        "invoice_number": "1234",
        "invoice_currency": "EUR",
        "invoice_tax_amount": 10,
        "transmission_format": "FPA12",
        "recipient_address": {
            "address": "Via Roma",
            "postcode": "50123",
            "city": "Florence",
            "country_code": "IT",
        },
        "invoice_type": "TD01",
        "invoice_tax_rate": 22.0,
        "invoice_date": date.today().isoformat(),
        "invoice_deadline": (date.today() + timedelta(days=30)).isoformat(),
        "items": [
            {
                "description": "Sample item",
                "unit_price": 30,
                "quantity": 1,
                "vat_rate": 22.0,
            }
        ],
        "invoice_amount": 30,
        "recipient_first_name": "Patrick",
        "recipient_last_name": "Patrick",
        "payment_condition": "TP02",
        "payment_method": "MP08",
    }

    if code:
        data["recipient_code"] = code

    if pec:
        data["recipient_pec"] = pec

    response = api_client.post(reverse("invoice-list"), data, format="json")

    assert response.status_code == 201

    invoice = Invoice.objects.first()

    assert invoice.recipient_code == (code if code is not None else "")
    assert invoice.recipient_pec == (pec if pec is not None else "")


def test_updates_invoice_when_re_uploading(api_client, user, sender):
    api_client.force_login(user)

    data = {
        "invoice_number": "1234",
        "invoice_currency": "EUR",
        "invoice_tax_amount": 10,
        "transmission_format": "FPA12",
        "recipient_address": {
            "address": "Via Roma",
            "postcode": "50123",
            "city": "Florence",
            "country_code": "IT",
        },
        "invoice_type": "TD01",
        "invoice_tax_rate": 22.0,
        "invoice_date": date.today().isoformat(),
        "invoice_deadline": (date.today() + timedelta(days=30)).isoformat(),
        "invoice_amount": 30,
        "recipient_code": "XXXXXXX",
        "items": [
            {
                "description": "Sample item",
                "unit_price": 30,
                "quantity": 1,
                "vat_rate": 22.0,
            }
        ],
        "recipient_denomination": "Example srl",
        "payment_condition": "TP02",
        "payment_method": "MP08",
    }

    response = api_client.post(reverse("invoice-list"), data, format="json")
    assert response.status_code == 201

    data["invoice_tax_amount"] = 100

    response = api_client.post(reverse("invoice-list"), data, format="json")
    assert response.status_code == 201

    assert Invoice.objects.count() == 1
    invoice = Invoice.objects.first()

    assert invoice.invoice_tax_amount == Decimal("100.00")
    assert invoice.items.count() == 1

    item = invoice.items.first()
    assert item.description == "Sample item"
