from django.urls import path
from .views import (
    PackageListView,
)


app_name = 'package'
urlpatterns = [
    path('', PackageListView.as_view(), name='list'),
]
