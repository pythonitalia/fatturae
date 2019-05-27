from __future__ import annotations

import decimal
from typing import TYPE_CHECKING, Dict, List, Union

from lxml import etree

from .types import ProductSummary, XMLDict
from .utils import dict_to_xml, format_price


if TYPE_CHECKING:
    from invoices.models import Invoice, Sender, Address


NAMESPACE_MAP = {
    "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

SCHEMA_LOCATION = (
    "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 "
    "http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2"
    "/Schema_del_file_xml_FatturaPA_versione_1.2.xsd"
)


def _get_price_minus_tax(
    price: Union[float, decimal.Decimal], invoice: Invoice
) -> float:
    return decimal.Decimal(price) / (1 + invoice.invoice_tax_rate / 100)


def get_invoice_summary(invoice: Invoice) -> Dict[str, str]:
    taxable_amount = _get_price_minus_tax(invoice.invoice_amount, invoice)
    tax = invoice.invoice_amount - taxable_amount

    return {
        "AliquotaIVA": format_price(invoice.invoice_tax_rate),
        "ImponibileImporto": format_price(taxable_amount),
        "Imposta": format_price(tax),
    }


def _get_recipient_code(invoice: Invoice) -> str:
    if not invoice.recipient_code:
        return "0000000"

    return invoice.recipient_code


def _generate_header(invoice: Invoice) -> XMLDict:
    sender: Sender = invoice.sender
    address: Address = sender.address
    client_address: Address = invoice.recipient_address

    header: XMLDict = {
        "FatturaElettronicaHeader": {
            "DatiTrasmissione": {
                "IdTrasmittente": {
                    "IdPaese": sender.country_code,
                    "IdCodice": sender.code,
                },
                "ProgressivoInvio": 1,
                "FormatoTrasmissione": invoice.transmission_format,
                "CodiceDestinatario": _get_recipient_code(invoice),
                "PecDestinatario": invoice.recipient_pec,
            },
            "CedentePrestatore": {
                "DatiAnagrafici": {
                    "IdFiscaleIVA": {
                        "IdPaese": sender.country_code,
                        "IdCodice": sender.code,
                    },
                    "Anagrafica": {"Denominazione": sender.company_name},
                    "RegimeFiscale": sender.tax_regime,
                },
                "Sede": {
                    "Indirizzo": address.address,
                    "CAP": address.postcode,
                    "Comune": address.city,
                    "Provincia": address.province,
                    "Nazione": address.country_code,
                },
            },
            "CessionarioCommittente": {
                "DatiAnagrafici": {
                    "CodiceFiscale": invoice.recipient_fiscal_code,
                    "IdFiscaleIVA": {
                        "IdPaese": sender.country_code,
                        "IdCodice": invoice.recipient_tax_code,
                    }
                    if not invoice.recipient_fiscal_code
                    else {},
                    "Anagrafica": {
                        "Denominazione": invoice.recipient_denomination,
                        "Nome": invoice.recipient_first_name,
                        "Cognome": invoice.recipient_last_name,
                    },
                },
                "Sede": {
                    "Indirizzo": client_address.address,
                    "CAP": client_address.postcode,
                    "Comune": client_address.city,
                    "Provincia": client_address.province,
                    "Nazione": client_address.country_code,
                },
            },
        }
    }

    return header


def _generate_body(invoice: Invoice) -> XMLDict:
    summary: List[ProductSummary] = invoice.invoice_summary

    body: XMLDict = {
        "FatturaElettronicaBody": {
            "DatiGenerali": {
                "DatiGeneraliDocumento": {
                    "TipoDocumento": invoice.invoice_type,
                    "Divisa": invoice.invoice_currency,
                    "Data": invoice.invoice_date.strftime("%Y-%m-%d"),
                    "Numero": invoice.invoice_number,
                    "Causale": invoice.causal,
                }
            },
            "DatiBeniServizi": {
                "DettaglioLinee": [
                    {
                        "NumeroLinea": x["row"],
                        "Descrizione": x["description"],
                        "Quantita": format_price(x["quantity"]),
                        "PrezzoUnitario": format_price(
                            _get_price_minus_tax(x["unit_price"], invoice)
                        ),
                        "PrezzoTotale": format_price(
                            _get_price_minus_tax(x["total_price"], invoice)
                        ),
                        "AliquotaIVA": format_price(x["vat_rate"]),
                    }
                    for x in summary
                ],
                "DatiRiepilogo": get_invoice_summary(invoice),
            },
            "DatiPagamento": {
                "CondizioniPagamento": invoice.payment_condition,
                "DettaglioPagamento": {
                    "ModalitaPagamento": invoice.payment_method,
                    "ImportoPagamento": format_price(invoice.invoice_amount),
                },
            },
        }
    }

    return body


def invoice_to_xml(invoice: Invoice) -> etree._Element:
    root_tag = "{%s}FatturaElettronica" % NAMESPACE_MAP["p"]
    schema_location_key = "{%s}schemaLocation" % NAMESPACE_MAP["xsi"]

    root = etree.Element(
        root_tag,
        attrib={schema_location_key: SCHEMA_LOCATION},
        nsmap=NAMESPACE_MAP,
        versione="FPR12",
    )

    header = _generate_header(invoice)
    body = _generate_body(invoice)

    tags = [*dict_to_xml(header), *dict_to_xml(body)]

    for tag in tags:
        root.append(tag)

    return root
