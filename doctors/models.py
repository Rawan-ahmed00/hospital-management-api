from django.db import models


class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dentistry', 'Dentistry'),
        ('Dermatology', 'Dermatology'),
        ('Neurology', 'Neurology'),
        ('Pediatrics', 'Pediatrics'),
        ('Orthopedics', 'Orthopedics'),
        ('General', 'General'),
    ]

    name = models.CharField(max_length=100)
    specialty = models.CharField(
        max_length=50,
        choices=SPECIALTY_CHOICES
    )
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    experience_years = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
