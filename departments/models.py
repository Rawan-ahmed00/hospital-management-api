from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    floor = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self
