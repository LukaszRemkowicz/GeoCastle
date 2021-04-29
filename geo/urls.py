from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView

from profiles.views import ProfileFollowToggle, register, activate_user_view

from django.conf.urls.static import static
from profiles import views as user_views
from mail import views as mail_views





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('measurements.urls', namespace='measurements')),
    path('register/', user_views.register, name='register'),
    re_path(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    # path('login/', LoginView.as_view(), name='login'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('profile-follow/', ProfileFollowToggle.as_view(), name='follow'),
    # path('u/', include('profiles.urls')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    # path('contact/', TemplateView.as_view(template_name='contact_form.html'), name='contact'),
    # path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('squad/', TemplateView.as_view(template_name='squad.html'), name='squad'),

    path('contact/', mail_views.contactView, name='contact'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('team/', TemplateView.as_view(template_name='team.html'), name='team'),

    path('your_profile/', include('profiles.urls', namespace='user_profile')),
    path('account_settings/', include('profiles.urls', namespace='account_settings')),
    path('change_password/', user_views.change_password, name='change_password'),
    path('', include('mail.urls')),
    re_path(r's/$', user_views.search, name='search'),
    re_path(r'user/$', user_views.load_user_profile, name='users_profile')

]

if settings.DEBUG:
    urlpatterns += static(settings .MEDIA_URL, document_root=settings.MEDIA_ROOT)