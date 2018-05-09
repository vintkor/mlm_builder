from django.urls import path
from .views import (
    WebinarListView,
    WebinarDetailView,
    WebinarUpdateView,
    WebinarCreateView,
    WebinarDeleteView,
)


app_name = 'webinar'
urlpatterns = [
    path('', WebinarListView.as_view(), name='my_webinars'),
    path('<slug:slug>/<int:owner_pk>', WebinarDetailView.as_view(), name='detail'),
    path('<slug:slug>/update', WebinarUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete', WebinarDeleteView.as_view(), name='delete'),
    path('create', WebinarCreateView.as_view(), name='create'),
]
