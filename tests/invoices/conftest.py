import os
from typing import List

import pytest

from invoices.models import Address, Sender
from invoices.xml.types import ProductSummary
from lxml import etree


@pytest.fixture
def sample_invoice_xml():
    here = os.path.dirname(__file__)

    parser = etree.XMLParser(remove_blank_text=True)

    root = etree.parse(
        os.path.join(here, "../data/IT01234567890_FPA01.xml"), parser=parser
    )

    for elem in root.iter("*"):
        if elem.text is not None:
            elem.text = elem.text.strip()

    return root


@pytest.fixture
def supplier_address():
    return Address.objects.create(
        address="Via Mugellese 1/A",
        city="Campi Bisenzio",
        postcode="50013",
        province="FI",
        country_code="IT",
    )


@pytest.fixture
def client_address():
    return Address.objects.create(
        address="Via Roma 1",
        city="Avellino",
        postcode="83100",
        province="AV",
        country_code="IT",
    )


@pytest.fixture
def sender(supplier_address):
    return Sender.objects.create(
        name="Python Italia APS",
        code="PIABCDE",
        country_code="IT",
        contact_phone="+390123456789",
        contact_email="info@python.it",
        company_name="Python Italia APS",
        tax_regime="RF01",
        address=supplier_address,
    )


@pytest.fixture
def sample_summary() -> List[ProductSummary]:
    return [
        {
            "row": 1,
            "description": "item 1",
            "quantity": "1",
            "unit_price": "1",
            "total_price": "1",
            "vat_rate": "0",
        },
        {
            "row": 2,
            "description": "item 2",
            "quantity": "2",
            "unit_price": "2",
            "total_price": "2",
            "vat_rate": "0",
        },
    ]
