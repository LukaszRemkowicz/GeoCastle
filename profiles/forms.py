from collections import OrderedDict

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django.core.checks import messages
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Profile

User = get_user_model()


# class ChangePassword(forms.Form):
#     old_password = forms.PasswordInput(attrs={'type': "password", 'class': "form-control"})
#     new_password = forms.PasswordInput(attrs={'type': "password", 'class': "form-control"})
#     reenter_password = forms.PasswordInput(attrs={'type': "password", 'class': "form-control"})
#
#     def clean(self):
#         new_password = self.cleaned_data.get('new_password')
#         reenter_password = self.cleaned_data.get('reenter_password')
#         old_password = self.cleaned_data.get('old_password')
#         if old_password != Profile.password:
#             pass
#         if new_password != reenter_password:
#             raise forms.ValidationError('Passwords are not the same')
#         if new_password == old_password or reenter_password == old_password:
#             raise forms.ValidationError('Passwords are not the same')
#             # get the user object and check from old_password list if any one matches with the new password raise error(read whole answer you would know)
#         return self.cleaned_data  # don't forget this.

# class PasswordChangeForms(SetPasswordForm):
#     """
#     A form that lets a user change their password by entering their old
#     password.
#     """
#     error_messages = dict(SetPasswordForm.error_messages, **{
#         'password_incorrect': _("Your old password was entered incorrectly. "
#                                 "Please enter it again."),
#     })
#     old_password = forms.CharField(label=_("Old password"),
#                                    widget=forms.PasswordInput)
#
#     def clean_old_password(self):
#         """
#         Validates that the old_password field is correct.
#         """
#         old_password = self.cleaned_data["old_password"]
#         if not self.user.check_password(old_password):
#             raise forms.ValidationError(
#                 self.error_messages['password_incorrect'],
#                 code='password_incorrect',
#             )
#         return old_password
#
#
# PasswordChangeForm.base_fields = OrderedDict(
#     (k, PasswordChangeForm.base_fields[k])
#     for k in ['old_password', 'new_password1', 'new_password2']
# )
#
# class Updatelast_login(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('last_login',)


class UpdateCountry(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('where_do_you_live',)

        # def save(self, *args, **kwargs):
        #     if getattr(self, 'country'):
        #         where_do_you_live = self.country
        #         self.relevant_field_name = pytesseract.image_to_string(Image.open(image_file))
        #     super(Component, self).save(*args, **kwargs)


class UserUpdateForm(forms.ModelForm):
    # OPTIONS = (('1', 'Poland'), ('2', 'Germany'))
    # country = forms.MultipleChoiceField(choices=OPTIONS)
    # country = CountryField().formfield(name_only=True)

    class Meta:
        model = Profile
        fields = ['name', 'birthday', 'email_when_someone_comment', 'email_when_someone_answer',
                  'email_when_someone_fallow', 'phone', 'website', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'type': "text", 'class': "form-control"}),
            # 'email': forms.TextInput(attrs={'type': "text", 'class': "form-control mb-1", 'value': 'email'}),
            'birthday': forms.TextInput(attrs={'class': "form-control", 'type': "date", 'name': "dateofbirth",
                                               'id': "dateofbirth"}),
            'email_when_someone_comment': forms.CheckboxInput(attrs={'type': "checkbox",
                                                                     'class': "switcher-input"}),
            'email_when_someone_answer': forms.CheckboxInput(attrs={'type': "checkbox",
                                                                    'class': "switcher-input"}),
            'email_when_someone_fallow': forms.CheckboxInput(attrs={'type': "checkbox",
                                                                    'class': "switcher-input"}),
            'phone': forms.TextInput(attrs={'type': "text", 'class': "form-control"}),
            'website': forms.TextInput(attrs={'type': "text", 'class': "form-control"}),
            'location': forms.TextInput(attrs={'type': "text", 'class': "form-control"}),
        }


class UserAvatar(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'type': "file", 'class': "account-settings-fileinput"})
        }


class UserEmailChange(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control", 'name': "username",
               'required': "required"})),
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'type': "text", 'class': "form-control", 'name': "email",
               'required': "required", 'style': "border: black;"})),
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'class': "form-control", 'name': "password",
               'required': "required"})),
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'class': "form-control", 'name': "password",
               'required': "required"})),

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control",
                                                             'placeholder': "login", 'required': "required"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type': "password", 'class': "form-control",
                                                                 'placeholder': "Password", 'required': "required"}))


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # fields = ['password1', 'password2']
    # widgets = {
    #     'password1': forms.CharField(attrs={
    #         'label': 'Password', }),
    #     'password2': forms.CharField(attrs={'label': 'Password confirmation'})
    # }
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('Cannot use this email. It\'s already registered.')
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # create a new user hash for activating email.

        if commit:
            user.save()
            user.profile.send_activation_email()
        return user
