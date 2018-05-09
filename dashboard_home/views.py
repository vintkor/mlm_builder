from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from images.models import UserImage
from webinar.models import Webinar, WebinarUser
from landing.models import Landing


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard_home/dashboard.html'
    context = {}

    def get(self, request):

        webinars = Webinar.objects.filter(owner=self.request.user, is_moderate=True)
        self.context['webinars_count'] = webinars.count()

        landing = Landing.objects.filter(owner=self.request.user)
        self.context['landing_count'] = landing.count()

        my_users = WebinarUser.objects.filter(owner=self.request.user)
        self.context['landing_get_users'] = my_users.count()

        my_images = UserImage.objects.filter(owner=request.user).count()
        self.context['my_images'] = my_images

        return render(request, self.template_name, self.context)
