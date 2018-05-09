from django.db.models import F
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from user_email.models import Email
from images.models import UserImage, LandingImage
from webinar.models import Webinar, WebinarUser
from .models import Landing
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from PIL import Image
from mlm_builder.settings import MEDIA_ROOT, MEDIA_URL
import os
from mlm_builder.settings import MEDIA_ROOT


class LandingDetailView(View):

    def get_object(self, pk):
        return get_object_or_404(Landing, pk=pk)

    def get(self, request, pk, webinar_slug, image_pk=None):
        landing = self.get_object(pk)
        context = {'landing': landing}

        if image_pk:
            image = get_object_or_404(UserImage, pk=image_pk)
            context['image'] = image

        return render(self.request, 'landing/landing-detail.html', context)

    def post(self, request, pk, webinar_slug, image_pk=None):
        email = request.POST.get('email').lower()

        landing = self.get_object(pk)

        users_in_webinar = WebinarUser.objects.filter(
            owner=landing.owner,
            webinar=landing.webinar,
            email=email,
            landing=landing,
        ).count()

        if users_in_webinar == 0:
            newWebinarUser = WebinarUser(
                owner=landing.owner,
                webinar=self.get_object(pk).webinar,
                email=email,
                landing=landing,
            )
            newWebinarUser.save()

            # return JsonResponse({'success': 1})

        user_email = Email.objects.filter(
            email=email, owner=landing.owner
        ).exists()

        if not user_email:
            try:
                new_user_email = Email(
                    email=email,
                    owner=landing.owner,
                )
                new_user_email.save()
            except:
                pass

            # Сохранение статистики по конкретному изображению
            if image_pk:
                landingimage = LandingImage.objects.get(
                    langing=landing,
                    userimage_id=image_pk,
                )
                landingimage.email_counter += 1
                landingimage.save(update_fields=('email_counter',))

        return JsonResponse({'success': 2})


class LandingListView(LoginRequiredMixin, ListView):
    template_name = 'landing/landing-list.html'
    context_object_name = 'landings'

    def get_queryset(self):
        landings = Landing.objects.filter(
            owner=self.request.user,
        )
        return landings

    def post(self, request):
        landing_id = int(request.POST.get('lendingId'))

        try:
            landing = Landing.objects.get(id=landing_id)
        except Landing.DoesNotExist:
            return JsonResponse({
                'error': 0,
                'message': 'Landing does not exist',
            })

        title = request.POST.get('title')
        description = request.POST.get('description')

        landing.title = title
        landing.description = description

        context = {
            'status': 1,
            'title': title,
            'description': description,
        }

        image_file = request.FILES.get('image')

        if image_file:
            image_x = int(float(request.POST.get('image_x')))
            image_y = int(float(request.POST.get('image_y')))
            image_width = int(float(request.POST.get('imageWidth')))
            image_height = int(float(request.POST.get('imageHeight')))

            ext = image_file.name.split('.')[-1]

            image = Image.open(image_file)
            cropped_image = image.crop((image_x, image_y, image_width + image_x, image_height + image_y))
            resized_image = cropped_image.resize((image_width, image_height), Image.ANTIALIAS)

            file_name = 'lendings/{}__{}.{}'.format(landing.id, get_random_string(length=30), ext)

            resized_image.save('{}/{}'.format(MEDIA_ROOT, file_name))

            landing.image = file_name
            context['image_url'] = MEDIA_URL + file_name

        landing.save(update_fields=('title', 'description', 'image'))

        return JsonResponse(context)


class LandingDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        """
        Удаление лендинга со всеми изображениями
        :param request: 
        :param pk: 
        :return: JsonResponse
        """
        landing = Landing.objects.get(id=pk)
        landing.delete()

        path = MEDIA_ROOT + '/lendings/'
        files = os.listdir(path)

        for file in files:
            if int(file.split('__')[0]) == int(pk):
                os.remove(path + file)

        return JsonResponse({'success': 1})


class LandingEditView(DetailView):
    template_name = 'landing/landing-detail.html'
    context_object_name = 'landing'
    model = Landing


class LandingCreatePremium(View):

    def get(self, request, webinar_pk):
        webinar = Webinar.objects.values('title').get(id=webinar_pk)
        landing = Landing(
            title='Премиум лендинг к вебинару {}'.format(webinar['title']),
            owner=self.request.user,
            webinar_id=webinar_pk,
        )
        landing.save()

        return redirect(reverse_lazy('landing:edit', kwargs={'pk': landing.pk}))


class LandingEditPremium(DetailView):
    template_name = 'landing/premium_editor/index.html'
    context_object_name = 'lending'
    model = Landing

    def post(self, request, pk):
        if request.POST.get('imageWidth', False):
            image_width = int(float(request.POST.get('imageWidth')))
            image_height = int(float(request.POST.get('imageHeight')))
            image_x = int(float(request.POST.get('image_x')))
            image_y = int(float(request.POST.get('image_y')))
            image_file = request.FILES.get('image')

            ext = image_file.name.split('.')[-1]

            image = Image.open(image_file)
            cropped_image = image.crop((image_x, image_y, image_width + image_x, image_height + image_y))
            resized_image = cropped_image.resize((image_width, image_height), Image.ANTIALIAS)

            file_name = 'lendings/{}__{}.{}'.format(pk, get_random_string(length=10), ext)

            resized_image.save('{}/{}'.format(MEDIA_ROOT, file_name))

            return JsonResponse({
                'status': 1,
                'image_url': MEDIA_URL + file_name
            })

        if request.POST.get('save-page', False):
            """Сохранение HTML страници"""

            lending = self.get_object()
            lending.landing_HTML = request.POST.get('html', ' ')
            lending.save(update_fields=('landing_HTML',))

            return JsonResponse({'status': 1})

        return JsonResponse({'status': 0})
