import pytest

from lxml import etree

from invoices.models import Invoice, Sender, Address


def _xml_to_string(xml):
    return etree.tostring(xml, pretty_print=True).decode("utf-8")


@pytest.mark.xfail
def test_xml_generation(sample_invoice_xml):
    invoice = Invoice()

    invoice_xml = _xml_to_string(invoice.to_xml())
    sample_xml = _xml_to_string(sample_invoice_xml)

    assert invoice_xml == sample_xml


@pytest.mark.django_db
def test_xml_header_generation():
    pi_address = Address.objects.create(
        address="Via Mugellese 1/A",
        city="Campi Bisenzio",
        postcode="50013",
        province="FI",
        country_code="IT",
    )

    sender = Sender.objects.create(
        name="Python Italia APS",
        code="PIABCDE",
        country_code="IT",
        contact_phone="+390123456789",
        contact_email="info@python.it",
        company_name="Python Italia APS",
        tax_regime="RF01",
        address=pi_address,
    )

    client_address = Address.objects.create(
        address="Via Roma 1",
        city="Avellino",
        postcode="83100",
        province="AV",
        country_code="IT",
    )

    invoice = Invoice(
        sender=sender,
        invoice_number="00001A",
        transmission_format="FPR12",
        recipient_code="ABCDEFG",
        recipient_tax_code="AAABBB12B34Z123D",
        recipient_first_name="Patrick",
        recipient_last_name="A",
        recipient_address=client_address,
    )

    xml = invoice.to_xml()

    assert xml is not None

    header = xml.xpath(
        "/p:FatturaElettronica/FatturaElettronicaHeader",
        namespaces={
            "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2"
        },
    )[0]

    t_data = header.xpath("DatiTrasmissione")[0]

    assert t_data.xpath("IdTrasmittente/IdPaese")[0].text == "IT"
    assert t_data.xpath("IdTrasmittente/IdCodice")[0].text == "PIABCDE"
    assert t_data.xpath("ProgressivoInvio")[0].text == "00001A"
    assert t_data.xpath("FormatoTrasmissione")[0].text == "FPR12"
    # TODO: test PEC address
    assert t_data.xpath("CodiceDestinatario")[0].text == "ABCDEFG"

    # TODO: might need to add this to the invoice, in order to be able to
    # TODO: use different party for invoices (if ever needed)

    # Supplier data

    s_data = header.xpath("CedentePrestatore/DatiAnagrafici")[0]

    assert s_data.xpath("IdFiscaleIVA/IdPaese")[0].text == "IT"

    # TODO: add this to the model if it is the P. IVA
    # assert s_data.xpath("IdFiscaleIVA/IdCodice")[0].text == "IT"

    assert s_data.xpath("RegimeFiscale")[0].text == "RF01"
    assert (
        s_data.xpath("Anagrafica/Denominazione")[0].text == "Python Italia APS"
    )

    a_data = header.xpath("CedentePrestatore/Sede")[0]

    assert a_data.xpath("Indirizzo")[0].text == "Via Mugellese 1/A"
    assert a_data.xpath("CAP")[0].text == "50013"
    assert a_data.xpath("Comune")[0].text == "Campi Bisenzio"
    assert a_data.xpath("Provincia")[0].text == "FI"
    assert a_data.xpath("Nazione")[0].text == "IT"

    # Client data

    c_data = header.xpath("CessionarioCommittente/DatiAnagrafici")[0]

    assert c_data.xpath("CodiceFiscale")[0].text == "AAABBB12B34Z123D"
    assert c_data.xpath("Anagrafica/Nome")[0].text == "Patrick"
    assert c_data.xpath("Anagrafica/Cognome")[0].text == "A"

    ca_data = header.xpath("CessionarioCommittente/Sede")[0]

    assert ca_data.xpath("Indirizzo")[0].text == "Via Roma 1"
    assert ca_data.xpath("CAP")[0].text == "83100"
    assert ca_data.xpath("Comune")[0].text == "Avellino"
    assert ca_data.xpath("Provincia")[0].text == "AV"
    assert ca_data.xpath("Nazione")[0].text == "IT"
