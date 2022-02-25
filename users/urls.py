from django.urls import path
from users.views import UserListCreateView, UserRUDView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('<int:pk>/', UserRUDView.as_view()),
]
