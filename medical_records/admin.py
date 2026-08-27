from django.contrib import admin
from .models import MedicalRecord


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient',
        'doctor',
        'diagnosis',
        'record_date',
    )

    list_filter = (
        'record_date',
    )

    search_fields = (
        'patient__name',
        'doctor__name',
        'diagnosis',
    )
