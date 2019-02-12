from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.contrib import admin

from .models import Sender, Address, Invoice, Item, Retention, WelfareFund
from .utils import zip_files, xml_to_string


def invoice_export_to_xml(modeladmin, request, queryset):
    if len(queryset) == 1:
        model = queryset[0]
        file = xml_to_string(model.to_xml())
        response = HttpResponse(file, content_type='text/xml')
        response['Content-Disposition'] = f'attachment; filename={model.get_filename()}'
        response['Content-Length'] = len(file)
        return response

    files = []
    for model in queryset:
        files.append((model.get_filename(), xml_to_string(model.to_xml())))
    archive = zip_files(files)
    response = HttpResponse(archive, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=invoices.zip'
    response['Content-Length'] = len(archive)
    return response


invoice_export_to_xml.short_description = _('Export as xml')  # type: ignore


class InvoiceItemInline(admin.StackedInline):
    model = Item
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    actions = [invoice_export_to_xml]
    exclude = ('items', )
    inlines = [InvoiceItemInline]


admin.site.register(Sender)
admin.site.register(Address)
admin.site.register(Item)
admin.site.register(Retention)
admin.site.register(WelfareFund)
