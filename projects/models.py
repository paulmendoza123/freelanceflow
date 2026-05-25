from django.db import models

# Create your models here.
from django.db import models
from clients.models import Client

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('done', 'Done'),
    ]
    client      = models.ForeignKey(Client, on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    budget      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline    = models.DateField(null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title