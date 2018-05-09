from django.urls import path
from .views import (
    LandingListView,
    LandingDeleteView,
    LandingEditView,
    LandingCreatePremium,
    LandingEditPremium,
)


app_name = 'landing'
urlpatterns = [
    path('<int:pk>', LandingEditView.as_view(), name='detail'),
    path('create/<int:webinar_pk>', LandingCreatePremium.as_view(), name='create'),
    path('edit/<int:pk>/', LandingEditPremium.as_view(), name='edit'),
    path('', LandingListView.as_view(), name='list'),
    path('<int:pk>/delete', LandingDeleteView.as_view(), name='delete'),
]
