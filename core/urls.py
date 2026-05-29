"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from clients.views  import ClientViewSet
from projects.views import ProjectViewSet
from invoices.views import InvoiceViewSet
from timelogs.views import TimeLogViewSet

router = DefaultRouter()
router.register(r'clients',  ClientViewSet,  basename='client')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'timelogs', TimeLogViewSet, basename='timelog')

# ── Register View ──────────────────────────────────────────
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        email    = request.data.get('email', '').strip()
        password = request.data.get('password', '')
        confirm  = request.data.get('confirm_password', '')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=400)
        if password != confirm:
            return Response({'error': 'Passwords do not match.'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken.'}, status=400)
        if email and User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered.'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': f'Account created! Welcome, {user.username}.'}, status=201)

# ── Forgot Password View ───────────────────────────────────
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username     = request.data.get('username', '').strip()
        new_password = request.data.get('new_password', '')
        confirm      = request.data.get('confirm_password', '')

        if not username or not new_password:
            return Response({'error': 'Username and new password are required.'}, status=400)
        if new_password != confirm:
            return Response({'error': 'Passwords do not match.'}, status=400)
        if len(new_password) < 6:
            return Response({'error': 'Password must be at least 6 characters.'}, status=400)

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful! You can now login.'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Username not found.'}, status=404)

urlpatterns = [
    path('admin/',                  admin.site.urls),
    path('api/',                    include(router.urls)),
    path('api/auth/login/',         TokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/auth/refresh/',       TokenRefreshView.as_view(),     name='token_refresh'),
    path('api/auth/register/',      RegisterView.as_view(),         name='register'),
    path('api/auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
]