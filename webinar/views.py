from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from .models import Webinar, WebinarUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import WebinarUpdateForm, WebinarCreateForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from landing.models import Landing
from django.db.transaction import atomic


class WebinarListView(LoginRequiredMixin, ListView):
    template_name = 'webinar/webinar-list.html'
    context_object_name = 'webinars'

    def get_queryset(self):
        webinars = Webinar.objects.select_related('owner').prefetch_related('landing_set').filter(
            # is_moderate=True,
            # active_start_date__lte=datetime.datetime.now(),
            # active_end_date__gte=datetime.datetime.now(),
            owner=self.request.user,
        )
        return webinars


class WebinarPublicDetailView(View):
    template_name = 'webinar/webinar-detail.html'
    context = {}

    def get(self, request, code, **kwargs):
        webinar = WebinarUser.objects.select_related('webinar').get(code=code).webinar
        self.context['webinar'] = webinar
        return render(request, self.template_name, self.context)


class WebinarDetailView(LoginRequiredMixin, DetailView):
    template_name = 'webinar/webinar-detail.html'
    context_object_name = 'webinar'

    def get_object(self, **kwargs):

        webinar = Webinar.objects.prefetch_related('webinaruser_set').get(
            slug=self.kwargs.get('slug'),
            owner__id=self.kwargs.get('owner_pk'),
        )

        return webinar


class WebinarUpdateView(UpdateView):
    template_name = 'webinar/webinar-update.html'
    form_class = WebinarUpdateForm

    def get_object(self, **kwargs):
        return Webinar.objects.get(slug=self.kwargs.get('slug'))

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class WebinarCreateView(LoginRequiredMixin, CreateView):
    template_name = 'webinar/webinar-update.html'
    form_class = WebinarCreateForm
    model = Webinar

    def get(self, request, *args, **kwargs):
        if self.request.user.profile.is_can_create_webinar():
            return super(WebinarCreateView, self).get(request, *args, **kwargs)
        else:
            messages.error(self.request, 'У Вас закончилась квота на создание вебинаров', 'danger')
            return redirect(reverse_lazy('package:list'))

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        webinar = form.save(commit=False)
        webinar.owner = self.request.user
        webinar.save()
        return redirect(reverse_lazy('webinar:detail', kwargs={'slug': webinar.slug, 'owner_pk': webinar.owner.id}))


class WebinarDeleteView(View):

    def post(self, request, slug):
        webinar = Webinar.objects.get(slug=slug)
        lengings = Landing.objects.filter(webinar=webinar)

        with atomic():
            webinar.delete()
            lengings.delete()

        return JsonResponse({'success': 1})
