from django.db import models

# Create your models here.
from django.db import models
from projects.models import Project

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
    ]
    project    = models.ForeignKey(Project, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=50, unique=True)
    amount     = models.DecimalField(max_digits=10, decimal_places=2)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    due_date   = models.DateField(null=True, blank=True)
    created    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_no