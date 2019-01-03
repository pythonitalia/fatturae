from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.contrib import admin

from .models import Sender, Address, Invoice
from .utils import zip_files


def invoice_export_to_xml(modeladmin, request, queryset):
    if len(queryset) == 1:
        model = queryset[0]
        response = HttpResponse(model.to_xml(), content_type='text/xml')
        response['Content-Disposition'] = f'attachment; filename={model.get_filename()}'
        return response

    files = []
    for model in queryset:
        files.append((model.get_filename(), model.to_xml()))
    response = HttpResponse(zip_files(files), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=invoices.zip'
    return response


invoice_export_to_xml.short_description = _('Export as xml')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    actions = [invoice_export_to_xml]


admin.site.register(Sender)
admin.site.register(Address)
