from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = [
        ('HOT', 'Hot'),
        ('WARM', 'Warm'),
        ('COLD', 'Cold'),
    ]

    phone = models.CharField(max_length=30)
    message = models.TextField()
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} ({self.status})"


class Appointment(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    requested_text = models.TextField()
    scheduled_for = models.DateTimeField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.lead.phone}"