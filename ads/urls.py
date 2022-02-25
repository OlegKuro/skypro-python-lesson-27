from django.urls import path
from ads.views import index, AdsListCreate, CategoriesListCreate, CategoryRetrieveUpdateView, AdUpdateRetrieveView, UploadAdImageView

urlpatterns = [
    path('', index),
    path('cat/', CategoriesListCreate.as_view()),
    path('cat/<int:pk>/', CategoryRetrieveUpdateView.as_view()),
    path('ad/', AdsListCreate.as_view()),
    path('ad/<int:pk>/', AdUpdateRetrieveView.as_view()),
    path('ad/<int:pk>/upload_image', UploadAdImageView.as_view()),
]
