import os
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from landing.models import Landing
from .models import UserImage, LandingImage
from django.views.generic import ListView, DetailView
import requests
import json
from binascii import a2b_base64
from mlm_builder.settings import MEDIA_ROOT


class UserImageListView(ListView):
    """
    Список картинок пользователя
    """
    template_name = 'images/user-images-list-view.html'
    context_object_name = 'images'

    def get_queryset(self):
        return UserImage.objects.filter(owner=self.request.user)

    def get(self, *args, **kwargs):
        image_id = self.request.GET.get('get_image_info')
        if image_id:

            try:
                user_image = UserImage.objects.prefetch_related('landing').get(id=image_id)
            except UserImage.DoesNotExist:
                return Http404()

            context = {
                'landings': []
            }
            for landing in user_image.landing.all():
                landing_image = LandingImage.objects.get(langing=landing, userimage_id=image_id)
                context['landings'].append({
                    'id': landing.id,
                    'title': landing.title,
                    'link': landing.get_absolute_url(),
                    'image_id': image_id,
                    'set_title': landing_image.title,
                    'set_description': landing_image.description,
                })

            return JsonResponse(context)

        return super(UserImageListView, self).get(args, kwargs)


class ImageDetailView(DetailView):
    template_name = 'images/image-detail.html'
    context_object_name = 'image'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        image = UserImage.objects.get(pk=pk)
        return image

    def post(self, *args, **kwargs):

        if self.request.POST.get('imageToLanding'):
            data = [
                {
                    'id': 0,
                    'text': 'Выберите лендинг',
                    'disabled': True,
                    'selected': True
                }
            ]

            landingimages = [i['langing_id'] for i in LandingImage.objects.filter(
                userimage=self.get_object(),
            ).values('langing_id')]

            landings = Landing.objects.filter(
                owner=self.request.user
            )

            for landing in landings:
                data.append({
                    'id': landing.id,
                    'text': landing.title,
                    'disabled': True if landing.id in landingimages else False,
                })

            return JsonResponse({'data': data})

        response_data = {'success': 0}

        landing_id = self.request.POST.get('landing_id')
        image_id = self.request.POST.get('image_id')

        if landing_id and image_id:
            landing = get_object_or_404(Landing, pk=landing_id)
            image = get_object_or_404(UserImage, pk=image_id)
            landing_image = get_object_or_404(LandingImage, langing=landing, userimage=image)
            landing_image.delete()

            response_data.update({'success': 1})

        return JsonResponse(response_data)


class LandingToImage(View):
    """
    Связывание изображения и лендинга
    """

    def post(self, request):
        landing = get_object_or_404(Landing, pk=request.POST.get('landing'))
        image = get_object_or_404(UserImage, pk=request.POST.get('image'))
        title = request.POST.get('title')
        description = request.POST.get('description')

        landingimage = LandingImage(
            langing=landing,
            userimage=image,
            title=title,
            description=description,
        )
        landingimage.save()

        return redirect(request.META.get('HTTP_REFERER'))


class CreateNewimageView(DetailView):
    template_name = 'images/create-image.html'
    context_object_name = 'image'
    model = UserImage

    def post(self, request, pk):
        user_image = self.get_object()

        image_data_url = request.POST.get('imageData').split('data:image/png;base64,')[-1]
        binary_data = a2b_base64(image_data_url)
        filename = '{path}/{image_name}'.format(
            path=MEDIA_ROOT,
            image_name=user_image.image,
        )

        fd = open(filename, 'wb')
        fd.write(binary_data)
        fd.close()

        return JsonResponse({'status': 1})


class DeleteImage(View):
    """
    Удаление изображения из базы и из хранилища
    """

    def post(self, request, pk):
        print('-'*90)
        image = get_object_or_404(UserImage, id=pk)
        filename = image.image
        image.delete()

        path = MEDIA_ROOT + '/' + str(filename)
        os.remove(path)

        return JsonResponse({'status': True})


class SearchImageView(View):
    """
    Поиск картинок на Pixabey.com API 
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SearchImageView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        print('-'*80)

        print(request)
        if request.GET.get('action') == 'get_my_images':
            user_images = list(map(lambda x: x[0], UserImage.objects.filter(
                owner=request.user).values_list('image')))
            return JsonResponse({
                'status': True,
                'my_images': list(map(lambda x: int(x.split('__')[-1].split('.')[0]), user_images)),
            })

        return render(request, 'images/search-image.html')

    def post(self, request):
        url = json.loads(request.body.decode('utf-8')).get('url')
        image_id = json.loads(request.body.decode('utf-8')).get('image_id')

        if url:
            ext = self.get_file_ext(url)
            filename = self.make_filename(image_id, ext, self.request.user.id)

            user_images = list(map(lambda x: x[0], UserImage.objects.filter(owner=request.user).values_list('image')))

            if filename not in user_images:
                self.get_and_save_image(url, filename)

                image = UserImage(
                    owner=request.user,
                    image=filename,
                    title='Title not yet',
                )
                image.save()

                return JsonResponse({'status': True})

        return JsonResponse({'status': False})

    @staticmethod
    def get_and_save_image(url, filename):
        r = requests.get(url)
        if r.status_code == 200:
            with open('media/' + filename, 'wb') as file:
                file.write(r.content)

    @staticmethod
    def make_filename(pk, ext, user_id):
        return 'images/{}__{}.{}'.format(user_id, pk, ext)

    @staticmethod
    def get_file_ext(url):
        return url.split('.')[-1]
