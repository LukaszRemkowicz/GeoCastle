from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from . import views

from .views import contactView, successView, RequestPasswordResetEmail, CompletePasswordReset, SetNewPasswordView

urlpatterns = [
    path('contact/', contactView, name='contact'),
    path('success/', TemplateView.as_view(template_name='contact_form.html'), name='success'),
    path('reset_password/', RequestPasswordResetEmail.as_view(), name='reset_password'),
    path('set_newpassword/<uidb64>/<token>', SetNewPasswordView.as_view(), name='set_newpassword')
]