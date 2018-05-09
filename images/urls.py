from django.urls import path
from .views import (
    UserImageListView,
    CreateNewimageView,
    SearchImageView,
    DeleteImage,
    ImageDetailView,
    LandingToImage,
)


app_name = 'images'
urlpatterns = [
    path('', UserImageListView.as_view(), name='user-images-list'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='detail-image'),
    path('create-image/<int:pk>/', CreateNewimageView.as_view(), name='create-image'),
    path('delete-image/<int:pk>/', DeleteImage.as_view(), name='delete-image'),
    path('search-image/', SearchImageView.as_view(), name='search-image'),
    path('landing-to-image/', LandingToImage.as_view(), name='landing-to-image'),
]
