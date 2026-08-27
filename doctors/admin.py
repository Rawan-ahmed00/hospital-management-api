from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'specialty',
        'phone',
        'available',
    )

    search_fields = (
        'name',
        'specialty',
        'phone',
    )

    list_filter = (
        'specialty',
        'available',
    )
