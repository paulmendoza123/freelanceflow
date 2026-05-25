from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
  serializer_class   = ClientSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    # Users only see their own clients
    return Client.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user) 