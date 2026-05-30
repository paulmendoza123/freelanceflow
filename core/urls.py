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
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from pathlib import Path

from clients.views   import ClientViewSet
from projects.views  import ProjectViewSet
from invoices.views  import InvoiceViewSet
from timelogs.views  import TimeLogViewSet
from core.auth_views import register_view, forgot_password_view  

BASE_DIR = Path(__file__).resolve().parent.parent

router = DefaultRouter()
router.register(r'clients',  ClientViewSet,  basename='client')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'timelogs', TimeLogViewSet, basename='timelog')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/',                       include(router.urls)),
    path('api/auth/login/',            TokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/auth/refresh/',          TokenRefreshView.as_view(),     name='token_refresh'),
    path('api/auth/register/',         register_view,                  name='register_api'),        
    path('api/auth/forgot-password/',  forgot_password_view,           name='forgot_password_api'), 

    # Static files
    path('css/<path:path>', serve, {'document_root': BASE_DIR / 'frontend/css'}),
    path('js/<path:path>',  serve, {'document_root': BASE_DIR / 'frontend/js'}),

    # Frontend HTML pages
    path('',                     TemplateView.as_view(template_name='index.html'),           name='login'),
    path('dashboard.html',       TemplateView.as_view(template_name='dashboard.html'),       name='dashboard'),
    path('clients.html',         TemplateView.as_view(template_name='clients.html'),         name='clients'),
    path('projects.html',        TemplateView.as_view(template_name='projects.html'),        name='projects'),
    path('invoices.html',        TemplateView.as_view(template_name='invoices.html'),        name='invoices'),
    path('timelogs.html',        TemplateView.as_view(template_name='timelogs.html'),        name='timelogs'),
    path('forgot-password.html', TemplateView.as_view(template_name='forgot-password.html'),name='forgot_password'), 
    path('register.html',        TemplateView.as_view(template_name='register.html'),        name='register'),        
]