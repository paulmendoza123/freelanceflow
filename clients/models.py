from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    name    = models.CharField(max_length=200)
    email   = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    phone   = models.CharField(max_length=20, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name