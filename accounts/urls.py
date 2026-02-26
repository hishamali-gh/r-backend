from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('users/', views.UserAPIView.as_view()),
    path('users/<int:pk>/', views.UserAPIView.as_view())
]
