import pytest

from lxml import etree

from invoices.models import Invoice


def _xml_to_string(xml):
    return etree.tostring(xml, pretty_print=True).decode("utf-8")


def test_xml_generation(sample_invoice_xml):
    invoice = Invoice()

    invoice_xml = _xml_to_string(invoice.to_xml())
    sample_xml = _xml_to_string(sample_invoice_xml)

    assert invoice_xml == sample_xml
