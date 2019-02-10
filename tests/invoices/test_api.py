from django.urls import reverse


def test_fails_with_empty_data(api_client):
    response = api_client.post(reverse("invoice-list"), {}, format="json")

    assert response.status_code == 400
