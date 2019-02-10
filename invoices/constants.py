from model_utils import Choices
from pycountry import countries, currencies


COUNTRIES = Choices(
    *[(country.alpha_2, country.name) for country in countries]
)

CURRENCIES = Choices(
    *[(currency.alpha_3, currency.name) for currency in currencies]
)

TAX_REGIMES = Choices(
    ("RF01", "Ordinario"),
    ("RF02", "Contribuenti minimi (art.1, c.96-117, L. 244/07)"),
    ("RF03", "Nuove iniziative produttive (art.13, L. 388/00) "),
    (
        "RF04",
        "Agricoltura e attività connesse e pesca (artt.34 e 34-bis, DPR 633/72)",
    ),
    ("RF05", "Vendita sali e tabacchi (art.74, c.1, DPR. 633/72)"),
    ("RF06", "Commercio fiammiferi (art.74, c.1, DPR 633/72)"),
    ("RF07", "Editoria (art.74, c.1, DPR 633/72)"),
    ("RF08", "Gestione servizi telefonia pubblica (art.74, c.1, DPR 633/72)"),
    (
        "RF09",
        "Rivendita documenti di trasporto pubblico e di sosta (art.74, c.1, DPR 633/72)",
    ),
    (
        "RF10",
        "Intrattenimenti, giochi e altre attività di cui alla tariffa allegata al DPR 640/72 (art.74, c.6, DPR 633/72)",
    ),
    ("RF11", "Agenzie viaggi e turismo (art.74-ter, DPR 633/72) "),
    ("RF12", "Agriturismo (art.5, c.2, L. 413/91)"),
    ("RF13", "Vendite a domicilio (art.25-bis, c.6, DPR 600/73)"),
    (
        "RF14",
        "Rivendita beni usati, oggetti d’arte, d’antiquariato o da collezione (art.36, DL 41/95)",
    ),
    (
        "RF15",
        "Agenzie di vendite all’asta di oggetti d’arte, antiquariato o da collezione (art.40-bis, DL 41/95)",
    ),
    ("RF16", "IVA per cassa P.A. (art.6, c.5, DPR 633/72)"),
    ("RF17", "IVA per cassa (art. 32-bis, DL 83/2012)"),
    ("RF18", "Altro"),
    ("RF19", "Regime forfettario (art.1, c.54-89, L. 190/2014)"),
)


TRANSMISSION_FORMATS = Choices("FPA12", "FPR12")

PAYMENT_CONDITIONS = Choices(
    ("TP01", "pagamento a rate"),
    ("TP02", "pagamento completo"),
    ("TP03", "anticipo"),
)


INVOICE_TYPES = Choices(
    ("TD01", "fattura"),
    ("TD02", "acconto/anticipo su fattura"),
    ("TD03", "acconto/anticipo su parcella"),
    ("TD04", "nota di credito"),
    ("TD05", "nota di debito"),
    ("TD06", "parcella"),
)

PAYMENT_METHODS = Choices(
    ("MP01", "contanti"),
    ("MP02", "assegno"),
    ("MP03", "assegno circolare"),
    ("MP04", "contanti presso Tesoreria"),
    ("MP05", "bonifico"),
    ("MP06", "vaglia cambiario"),
    ("MP07", "bollettino bancario"),
    ("MP08", "carta di pagamento"),
    ("MP09", "RID"),
    ("MP10", "RID utenze"),
    ("MP11", "RID veloce"),
    ("MP12", "RIBA"),
    ("MP13", "MAV"),
    ("MP14", "quietanza erario"),
    ("MP15", "giroconto su conti di contabilità speciale"),
    ("MP16", "domiciliazione bancaria"),
    ("MP17", "domiciliazione postale"),
    ("MP18", "bollettino di c/c postale"),
    ("MP19", "SEPA Direct Debit"),
    ("MP20", "SEPA Direct Debit CORE"),
    ("MP21", "SEPA Direct Debit B2B"),
    ("MP22", "Trattenuta su somme già riscosse"),
)

WELFARE_FUND_TYPES = Choices(
    (
        "TC01",
        "Cassa nazionale previdenza e assistenza avvocati e procuratori legali",
    ),
    ("TC02", "Cassa previdenza dottori commercialisti"),
    ("TC03", "Cassa previdenza e assistenza geometri"),
    (
        "TC04",
        "Cassa nazionale previdenza e assistenza ingegneri e architetti liberi professionisti",
    ),
    ("TC05", "Cassa nazionale del notariato"),
    (
        "TC06",
        "Cassa nazionale previdenza e assistenza ragionieri e periti commerciali",
    ),
    (
        "TC07",
        "Ente nazionale assistenza agenti e rappresentanti di commercio (ENASARCO)",
    ),
    (
        "TC08",
        "Ente nazionale previdenza e assistenza consulenti del lavoro (ENPACL)",
    ),
    ("TC09", "Ente nazionale previdenza e assistenza medici (ENPAM)"),
    ("TC10", "Ente nazionale previdenza e assistenza farmacisti (ENPAF)"),
    ("TC11", "Ente nazionale previdenza e assistenza veterinari (ENPAV)"),
    (
        "TC12",
        "Ente nazionale previdenza e assistenza impiegati dell'agricoltura (ENPAIA)",
    ),
    (
        "TC13",
        "Fondo previdenza impiegati imprese di spedizione e agenzie marittime",
    ),
    ("TC14", "Istituto nazionale previdenza giornalisti italiani (INPGI)"),
    ("TC15", "Opera nazionale assistenza orfani sanitari italiani (ONAOSI)"),
    (
        "TC16",
        "Cassa autonoma assistenza integrativa giornalisti italiani (CASAGIT)",
    ),
    (
        "TC17",
        "Ente previdenza periti industriali e periti industriali laureati (EPPI)",
    ),
    ("TC18", "Ente previdenza e assistenza pluricategoriale (EPAP)"),
    ("TC19", "Ente nazionale previdenza e assistenza biologi (ENPAB)"),
    (
        "TC20",
        "Ente nazionale previdenza e assistenza professione infermieristica (ENPAPI)",
    ),
    ("TC21", "Ente nazionale previdenza e assistenza psicologi (ENPAP)"),
    ("TC22", "INPS"),
)
