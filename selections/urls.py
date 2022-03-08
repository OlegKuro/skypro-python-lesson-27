from django.urls import path
from selections import views

urlpatterns = [
    path('', views.SelectionsListView.as_view()),
    path('create/', views.SelectionCreateView.as_view()),
    path('<int:pk>/', views.SelectionUpdateDeleteView.as_view()),
    path('<int:pk>/retrieve/', views.RetrieveSelectionView.as_view()),
]