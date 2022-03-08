from django.urls import path
from users.views import UserListCreateView, UserRUDView, UserCreateView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('<int:pk>/', UserRUDView.as_view()),
    path('register/', UserCreateView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
]
