from django.urls import path
from ads.views import BaseView

urlpatterns = [
    path('', BaseView.as_view()),
]
