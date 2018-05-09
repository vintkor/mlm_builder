from django.urls import path, include
from django.views.generic import TemplateView
from .views import (
    logout_view,
    ProfileDetailView,
    AuthView,
    ProfileEditView,
)


app_name = 'profile'
urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', ProfileDetailView.as_view(), name='detail'),
    path('edit/', ProfileEditView.as_view(), name='edit'),
]
