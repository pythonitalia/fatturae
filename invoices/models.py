import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from .constants import COUNTRIES, TAX_REGIMES, TRANSMISSIONS_FORMAT
from .xml import invoice_to_xml


class Address(models.Model):
    address = models.CharField(_("Address"), max_length=200)
    postcode = models.CharField(_("Post Code"), max_length=20, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    province = models.CharField(_("Province"), max_length=100, blank=True)
    country_code = models.CharField(
        _("Country Code"), max_length=2, choices=COUNTRIES
    )


class Sender(TimeStampedModel):
    """Model containing information about a Sender of an electronic invoice.

    Contains also the configuration for the SdI."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=100, unique=True)
    country_code = models.CharField(
        _("Country Code"), max_length=2, choices=COUNTRIES
    )

    contact_phone = models.CharField(_("Contact Phone"), max_length=20)
    contact_email = models.CharField(_("Contact Email"), max_length=200)

    fiscal_code = models.CharField(_("Fiscal Code"), max_length=16)
    code = models.CharField(_("Sender code"), max_length=7)

    company_name = models.CharField(_("Company Name"), max_length=10)

    tax_regime = models.CharField(
        _("Tax Regime"), choices=TAX_REGIMES, max_length=4
    )

    address = models.ForeignKey(
        Address, models.PROTECT, verbose_name=_("Address")
    )

    def __str__(self):
        return f"{self.name}"


class Invoice(TimeStampedModel):
    sender = models.ForeignKey(
        Sender, verbose_name=_("Sender"), on_delete=models.PROTECT
    )
    invoice_number = models.CharField(_("Invoice number"), max_length=100)
    transmission_format = models.CharField(
        _("Transmission format"), choices=TRANSMISSIONS_FORMAT, max_length=5
    )

    recipient_code = models.CharField(_("Recipient code"), max_length=7)
    recipient_pec = models.EmailField(_("Recipient PEC"), blank=True)

    def to_xml(self):
        return invoice_to_xml(self)
