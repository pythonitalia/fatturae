from __future__ import annotations

from typing import TYPE_CHECKING

from lxml import etree


from .types import XMLDict
from .utils import dict_to_xml

if TYPE_CHECKING:
    from .models import Invoice


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
    header: XMLDict = {
        "FatturaElettronicaHeader": {
            "DatiTrasmissione": {
                "IdTrasmittente": {"IdPaese": "IT", "IdCodice": "01234567890"},
                "ProgressivoInvio": "00001",
                "FormatoTrasmissione": "FPR12",
                "CodiceDestinatario": "AAAAAA",
            },
            "CedentePrestatore": {
                "DatiAnagrafici": {
                    "IdFiscaleIVA": {
                        "IdPaese": "IT",
                        "IdCodice": "01234567890",
                    },
                    "Anagrafica": {"Denominazione": "ALPHA SRL"},
                    "RegimeFiscale": "RF19",
                },
                "Sede": {
                    "Indirizzo": "VIALE ROMA 543",
                    "CAP": "07100",
                    "Comune": "SASSARI",
                    "Provincia": "SS",
                    "Nazione": "IT",
                },
            },
            "CessionarioCommittente": {
                "DatiAnagrafici": {
                    "CodiceFiscale": "09876543210",
                    "Anagrafica": {"Denominazione": "AMMINISTRAZIONE BETA"},
                },
                "Sede": {
                    "Indirizzo": "VIA TORINO 38-B",
                    "CAP": "00145",
                    "Comune": "ROMA",
                    "Provincia": "RM",
                    "Nazione": "IT",
                },
            },
        }
    }

    return header


def _generate_body(invoice: Invoice) -> XMLDict:
    body: XMLDict = {
        "FatturaElettronicaBody": {
            "DatiGenerali": {
                "DatiGeneraliDocumento": {
                    "TipoDocumento": "TD01",
                    "Divisa": "EUR",
                    "Data": "2017-01-18",
                    "Numero": 123,
                    "Causale": (
                        "LA FATTURA FA RIFERIMENTO AD UNA OPERAZIONE AAAA BBBBBBBBBBBBBBBBBB CCC DDDDDDDDDDDDDDD E FFFFFFFFFFFFFFFFFFFF GGGGGGGGGG HHHHHHH II LLLLLLLLLLLLLLLLL MMM NNNNN OO PPPPPPPPPPP QQQQ RRRR SSSSSSSSSSSSSS"
                        "SEGUE DESCRIZIONE CAUSALE NEL CASO IN CUI NON SIANO STATI SUFFICIENTI 200 CARATTERI AAAAAAAAAAA BBBBBBBBBBBBBBBBB"
                    ),
                },
                "DatiOrdineAcquisto": {
                    "RiferimentoNumeroLinea": 1,
                    "IdDocumento": 66685,
                    "NumItem": 1,
                    "CodiceCUP": "123abc",
                    "CodiceCIG": "456def",
                },
                "DatiContratto": {
                    "RiferimentoNumeroLinea": 1,
                    "IdDocumento": 123,
                    "Data": "2016-09-01",
                    "NumItem": "5",
                    "CodiceCUP": "123abc",
                    "CodiceCIG": "456def",
                },
                "DatiConvenzione": {
                    "RiferimentoNumeroLinea": 1,
                    "IdDocumento": 456,
                    "NumItem": "5",
                    "CodiceCUP": "123abc",
                    "CodiceCIG": "456def",
                },
                "DatiRicezione": {
                    "RiferimentoNumeroLinea": 1,
                    "IdDocumento": 789,
                    "NumItem": "5",
                    "CodiceCUP": "123abc",
                    "CodiceCIG": "456def",
                },
                "DatiTrasporto": {
                    "DatiAnagraficiVettore": {
                        "IdFiscaleIVA": {
                            "IdPaese": "IT",
                            "IdCodice": "24681012141",
                        },
                        "Anagrafica": {"Denominazione": "Trasporto spa"},
                    },
                    "DataOraConsegna": "2017-01-10T16:46:12.000+02:00",
                },
            },
            "DatiBeniServizi": {
                "DettaglioLinee": {
                    "NumeroLinea": 1,
                    "Descrizione": "DESCRIZIONE DELLA FORNITURA",
                    "Quantita": "5.00",
                    "PrezzoUnitario": "1.00",
                    "PrezzoTotale": "5.00",
                    "AliquotaIVA": "22.00",
                },
                "DatiRiepilogo": {
                    "AliquotaIVA": "22.00",
                    "ImponibileImporto": "5.00",
                    "Imposta": "1.10",
                    "EsigibilitaIVA": "I",
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


def invoice_to_xml(invoice: Invoice):
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
