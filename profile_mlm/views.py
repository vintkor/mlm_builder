from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import (
    logout,
    authenticate,
    login,
)
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .forms import (
    AuthForm,
    ProfileEditForm,
)
from django.views.generic import FormView
from mlm_builder.utils import set_filename
from django.core.files.storage import FileSystemStorage


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('profile:login'))


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profile_mlm/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return Profile.objects.select_related('user').get(user=self.request.user)


class AuthView(FormView):
    form_class = AuthForm
    template_name = 'profile_mlm/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))

        return super(AuthView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect(reverse_lazy('dashboard'))


class ProfileEditView(LoginRequiredMixin, FormView):
    form_class = ProfileEditForm
    template_name = 'profile_mlm/edit.html'
    success_url = reverse_lazy('profile:detail')

    def get_form_kwargs(self):
        kwargs = super(ProfileEditView, self).get_form_kwargs()
        desc_init = self.request.user.profile.description
        if desc_init:
            kwargs['desc_init'] = self.request.user.profile.description
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        user = self.request.user

        avatar_file = self.request.FILES.get('avatar')
        if avatar_file:
            filename = set_filename(None, avatar_file.name)
            fs = FileSystemStorage()
            file_name = fs.save(filename, avatar_file)
            user.profile.avatar = file_name
            user.save()
            return super().form_valid(form)

        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        user.profile.description = form.cleaned_data.get('description')

        user.profile.description = form.cleaned_data.get('description')
        user.profile.phone = form.cleaned_data.get('phone')
        user.profile.website = form.cleaned_data.get('website')
        user.profile.skype = form.cleaned_data.get('skype')

        user.profile.link_vkontakte = form.cleaned_data.get('link_vkontakte')
        user.profile.link_facebook = form.cleaned_data.get('link_facebook')
        user.profile.link_twitter = form.cleaned_data.get('link_twitter')
        user.profile.link_instagram = form.cleaned_data.get('link_instagram')
        user.profile.link_odnoklassniki = form.cleaned_data.get('link_odnoklassniki')
        user.profile.link_my_world = form.cleaned_data.get('link_my_world')

        user.save()

        return super().form_valid(form)
