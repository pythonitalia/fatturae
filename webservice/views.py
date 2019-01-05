import logging

from django.views.decorators.csrf import csrf_exempt

from spyne import Application, Integer, Iterable, ServiceBase, Unicode, rpc
from spyne.model import (
    AnyXml,
    Array,
    ComplexModel,
    DateTime,
    UnsignedInteger16,
    UnsignedLong,
)
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication


# from spyne.util.xml import parse_schema_file

# x = parse_schema_file(
#     "/Users/patrickarminio/Documents/personal/fattura-elettronica/webservice/data/TrasmissioneTypes_v1.1.xsd.xml"
# )

# print(x["http://www.fatturapa.gov.it/sdi/ws/trasmissione/v1.0/types"])


logging.basicConfig(level=logging.DEBUG)


class BetterSomething(ComplexModel):
    # schemaLocation
    __namespace__ = (
        "http://www.fatturapa.gov.it/sdi/ws/trasmissione/v1.0/types"
    )


class HelloWorldService(ServiceBase):
    @rpc(
        BetterSomething,
        _operation_name="RicevutaConsegnaFatture_Msg",
        _part_name="ricevuta",
        _returns=Unicode,
    )
    def say_hello(ctx, name):
        pass


application = Application(
    [HelloWorldService],
    name="TrasmissioneFatture",
    tns="http://www.fatturapa.gov.it/sdi/ws/trasmissione/v1.0",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)


ws = csrf_exempt(DjangoApplication(application))
