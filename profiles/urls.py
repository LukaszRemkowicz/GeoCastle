from django.urls import re_path

from . views import ProfileDetailView
from django.views.generic import TemplateView

from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('your_profile/', views.user_profile, name='your_profile'),
    path('', views.account_settings, name='account_settings'),
    re_path(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='detail'),
    path('', views.user_login, name='login'),
    path('change_password', views.change_password, name='change_password')

]
