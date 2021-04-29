from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.urls import reverse
from .utils import code_generator
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL


# User = get_user_model()


class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    activation_key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20, null=True)

    """ Model need to be rebuild. Need to be dropped columns duplicated from User model """

    # email = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=30, null=True)
    image = models.FileField(default='static/avatar1.png', upload_to='profile_pics')
    birthday = models.CharField(max_length=30, blank=True)
    # country = CountryField(default='')
    where_do_you_live = models.CharField(max_length=100, blank=True)
    email_when_someone_comment = models.BooleanField(default=False)
    email_when_someone_answer = models.BooleanField(default=False)
    email_when_someone_fallow = models.BooleanField(default=False)
    phone = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator()
            self.save()
            # path_ = reverse()
            path_ = reverse('activate', kwargs={"code": self.activation_key})
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {path_}'
            recipient_list = [self.user.email]
            html_message = f'<p>Activate your account here: {path_}</p>'
            print(html_message)
            # sent_mail = send_mail(
            #     subject,
            #     message,
            #     from_email,
            #     recipient_list,
            #     fail_silently=False,
            #     html_message=html_message
            # )
            sent_mail = False
            return sent_mail

#
# def post_save_user_reciever(sender, instance, created, *args, **kwargs):
#     if created:
#         profile, is_created = Profile.objects.get_or_create(user=instance)
#         default_user_profile = Profile.objects.get_or_create(user__id=1)[0]
#         default_user_profile.followers.add(instance)
#         profile.followers.add(default_user_profile.user)
#         profile.followers.add(2)


# post_save.connect(post_save_user_reciever, sender=User)
