"""mlm_builder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views.generic import TemplateView

from landing.views import LandingDetailView
from mlm_builder.settings import MEDIA_URL, MEDIA_ROOT, DEBUG
from django.conf.urls.static import static
from dashboard_home.views import DashboardView
from webinar.views import WebinarPublicDetailView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('dashboard/', include([
        path('', DashboardView.as_view(), name='dashboard'),
        path('profile/', include('profile_mlm.urls')),
        path('webinar/', include('webinar.urls')),
        path('packages/', include('package.urls')),
        path('lending/', include('landing.urls')),
        path('images/', include('images.urls')),
    ])),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('l/<int:pk>/<slug:webinar_slug>/', LandingDetailView.as_view(), name='webinar-view'),
    path('l/<int:pk>/<slug:webinar_slug>/<int:image_pk>/', LandingDetailView.as_view(), name='webinar-view'),
    path('w/<slug:code>/', WebinarPublicDetailView.as_view(), name='publick-webinar'),
    re_path(r'^datetimepicker/', include('datetimepicker.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)


if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
