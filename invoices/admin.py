from django.contrib import admin

from .models import Sender, Address, Invoice


admin.site.register(Sender)
admin.site.register(Address)
admin.site.register(Invoice)
