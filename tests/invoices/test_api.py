from datetime import date, timedelta

from django.urls import reverse


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
        },
        format="json",
    )

    assert response.status_code == 201
