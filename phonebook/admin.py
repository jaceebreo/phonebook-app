from django.contrib import admin
from . import models

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "telephone_number",
    )


admin.site.register(models.Contact, ContactAdmin)
