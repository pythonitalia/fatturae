from __future__ import annotations

from typing import TYPE_CHECKING, List

from lxml import etree

from .types import ProductSummary, XMLDict
from .utils import dict_to_xml

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
                "ProgressivoInvio": invoice.invoice_number,
                "FormatoTrasmissione": invoice.transmission_format,
                "CodiceDestinatario": invoice.recipient_code,
            },
            "CedentePrestatore": {
                "DatiAnagrafici": {
                    "IdFiscaleIVA": {
                        "IdPaese": sender.country_code,
                        "IdCodice": "01234567890",
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
                    "CodiceFiscale": invoice.recipient_tax_code,
                    "Anagrafica": {
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
                        "Quantita": "{:.2f}".format(x["quantity"]),
                        "PrezzoUnitario": "{:.2f}".format(x["unit_price"]),
                        "PrezzoTotale": "{:.2f}".format(x["total_price"]),
                        "AliquotaIVA": "{:.2f}".format(x["vat_rate"]),
                    }
                    for x in summary
                ],
                "DatiRiepilogo": {
                    "AliquotaIVA": invoice.invoice_tax_rate,
                    "ImponibileImporto": invoice.invoice_amount,
                    "Imposta": invoice.invoice_tax_amount,
                },
            },
            "DatiPagamento": {
                "CondizioniPagamento": "TP01",
                "DettaglioPagamento": {
                    "ModalitaPagamento": "MP01",
                    "DataScadenzaPagamento": "2017-02-18",
                    "ImportoPagamento": "6.10",
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

    return etree.tostring(root).decode('utf-8')
