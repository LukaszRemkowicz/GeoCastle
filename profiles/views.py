import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.checks import messages
from django.forms import forms
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View
from django.shortcuts import render, redirect
from django.contrib import messages
import folium
from OSMPythonTools.api import Api

from .forms import RegisterForm, UserAvatar, UserUpdateForm, UserRegisterForm, UserLoginForm, UpdateCountry, \
    UserEmailChange
# Updatelast_login
from .models import Profile
from measurements.models import Locations

User = get_user_model()


def load_user_profile(request):
    if request.method == 'GET':
        q = request.GET.get('u')
        users = User.objects.get(username=q)
        locations = Locations.objects.filter(user=users)
        follow = Profile.followers.through.objects.filter(profile_id=users.id).count()
        follows = Profile.following.through.objects.filter(profile_id=users.id).count()
        review_count = 0
        for location in locations:
            if location.review:
                review_count += 1

        context = {'users': users,
                   'locations': locations,
                   'location_count': locations.count(),
                   'review_count': review_count,
                   'follow': follow,
                   'follows': follows
                   }
        template = 'profiles/users_profile.html'
        return render(request, template, context)


def search(request):
    if request.method == 'GET':
        try:
            q = request.GET.get('q')
        except:
            q = None
        if q:
            try:
                search_result = Profile.objects.filter(user__username__icontains=q)
            except:
                search_result = None
            if search_result:
                context = {'search_result': search_result}

                template = 'profiles/results.html'
            else:
                context = {'search_result': search_result}
                template = 'profiles/error_search.html'
        else:
            context = {}
            template = 'home.html'
        return render(request, template, context)


def castle_review(request):
    user = User.objects.get(id=request.user.id)
    locations = Locations.objects.filter(user=user)
    locations_dict = {}
    for location in locations:
        locations_dict[location] = location.review

    return render(request, 'profiles/user_profile.html')


def user_profile(request):
    if request.method == 'POST':
        review = request.POST.get('labelowski')
        loc_id = request.POST.get('loc_id')
        delete_but = request.POST.get('delete_but')
        if delete_but and 'deleting' in delete_but:
            loc_id = re.sub(r'(deleting)(\d+)', r'\2', delete_but)
            locations = Locations.objects.get(id=int(loc_id))
            locations.review = ''
            locations.save(update_fields=['review'])
        if review and loc_id:
            locations = Locations.objects.get(id=int(loc_id))
            locations.review = review
            locations.save(update_fields=['review'])

    api = Api()
    m = folium.Map()

    user = User.objects.get(id=request.user.id)
    locations = Locations.objects.filter(user=user)
    # locations_dict = []
    # for location in locations:
    #     locations_dict.append((location.name, location.review))
    follow = Profile.followers.through.objects.filter(profile_id=user.id).count()
    follows = Profile.following.through.objects.filter(profile_id=user.id).count()
    review_count = 0
    locations_dict = []
    for location in locations:
        if location.review:
            review_count += 1
        locations_dict.append((location.name, location.review))
        castle_data = api.query(f'node/{location.ide}')
        print(location.state)
        if location.state == 'Wishlist':
            folium.Marker([castle_data.lat(), castle_data.lon()], tooltip=location.name,
                          icon=folium.Icon(color='lightblue', icon='fort-awesome', prefix='fa')).add_to(m)
        else:
            folium.Marker([castle_data.lat(), castle_data.lon()], tooltip=location.name,
                          icon=folium.Icon(color='orange', icon='fort-awesome', prefix='fa')).add_to(m)

    m = m._repr_html_()

    review_form = {
        'map': m,
        'review_count': review_count,
        'location_count': locations.count(),
        'follow': follow,
        'follows': follows,
        'review': locations,
    }

    return render(request, 'profiles/user_profile.html', review_form)


@login_required()
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(data=request.POST, user=request.user)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Your account has been updated')
            return redirect(request.path_info)
        else:
            messages.error(request, password_form.errors)

    else:
        password_form = PasswordChangeForm(data=request.POST, user=request.user)
    context = {
        'password_form': password_form,
    }

    return render(request, 'profiles/change_password.html', context)


@login_required
def account_settings(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user.profile)
        p_form = UserAvatar(request.POST, request.FILES, instance=request.user.profile)
        email_form = UserEmailChange(request.POST, instance=request.user)
        if u_form.is_valid() and p_form.is_valid() and email_form.is_valid():
            data = request.POST.copy()
            country = request.POST.get('country')
            data['where_do_you_live'] = country
            new_form = UpdateCountry(data, instance=request.user.profile)
            if new_form.is_valid():
                new_form.save()
            u_form.save()
            p_form.save()
            email_form.save()
        else:
            messages.info(request, 'Data is not valid')
        messages.success(request, 'Your account has been updated')
        return redirect(request.path_info)
    else:
        # u_form = UserUpdateForm(instance=request.user)
        p_form = UserAvatar(instance=request.user.profile)
        user = User.objects.get(id=request.user.id)
        email_form = UserEmailChange(initial={'email': user.email})
        profile = Profile.objects.filter(user=user).get()
        country_form = UpdateCountry(instance=request.user.profile,
                                     initial={'where_do_you_live': profile.where_do_you_live})
        u_form = UserUpdateForm(instance=request.user, initial={"name": profile.name,
                                                                'birthday': profile.birthday,
                                                                'country': profile.where_do_you_live,
                                                                'email_when_someone_comment': profile.email_when_someone_comment,
                                                                'email_when_someone_answer': profile.email_when_someone_answer,
                                                                'email_when_someone_fallow': profile.email_when_someone_fallow,
                                                                'phone': profile.phone,
                                                                'website': profile.website,
                                                                'location': profile.location
                                                                })
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'email_form': email_form,
            'country_form': country_form,
        }

        return render(request, 'profiles/settings.html', context)


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return redirect("/login")
    return redirect("/login")


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # last_login = Profile(last_login=datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))
            # user.last_login = datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
            # user.save(update_fields=['last_login'])

            return redirect('/')
        else:
            messages.info(request, 'username OR password is incorrect')
            return redirect('login')

    form = UserLoginForm
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/')
        else:
            messages.error(request, 'wrong parameters')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'registration/register.html'
#     success_url = '/'
#
#     def dispatch(self, *args, **kwargs):
#         # if self.request.user.is_authenticated:
#         #     return redirect("/logout")
#         return super(RegisterView, self).dispatch(*args, **kwargs)


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get('username')
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f'/u/{profile_.user.username}/')


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        return context
