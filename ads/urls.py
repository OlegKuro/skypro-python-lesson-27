from django.urls import path
from ads.views import (index, AdsListCreate, CategoriesListCreate, CategoryRetrieveUpdateView, AdUpdateRetrieveView,
                       UploadAdImageView, LocationViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('', index),
    path('cat/', CategoriesListCreate.as_view()),
    path('cat/<int:pk>/', CategoryRetrieveUpdateView.as_view()),
    path('ad/', AdsListCreate.as_view()),
    path('ad/<int:pk>/', AdUpdateRetrieveView.as_view()),
    path('ad/<int:pk>/upload_image', UploadAdImageView.as_view()),
] + router.urls
