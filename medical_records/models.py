from django.db import models
from doctors.models import Doctor
from patients.models import Patient


class MedicalRecord(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medical_records'
    )

    diagnosis = models.TextField()

    symptoms = models.TextField(blank=True)

    treatment = models.TextField(blank=True)

    notes = models.TextField(blank=True)

    record_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient.name} - {self.record_date}"
