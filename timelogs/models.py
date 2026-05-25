from django.db import models

# Create your models here.
from django.db import models
from projects.models import Project

class TimeLog(models.Model):
    project     = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    hours       = models.DecimalField(max_digits=5, decimal_places=2)
    date        = models.DateField()
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project} - {self.hours}hrs"