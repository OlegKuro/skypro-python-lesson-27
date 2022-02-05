from django.urls import path
from ads.views import index, AdsListCreate, CategoriesListCreate, DetailAd, DetailCategory

urlpatterns = [
    path('', index),
    path('cat/', CategoriesListCreate.as_view()),
    path('cat/<int:pk>/', DetailCategory.as_view()),
    path('ad/', AdsListCreate.as_view()),
    path('ad/<int:pk>/', DetailAd.as_view()),
]
