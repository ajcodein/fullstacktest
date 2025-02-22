# for bookings
from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.CharField(max_length=10)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'time')  # to prevent double-booking
