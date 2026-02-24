from django.urls import path, include
from . import views

urlpatterns = [
    path('product-type/', views.ProductTypeAPIView.as_view()),
    path('product-type/<int:pk>/', views.ProductTypeAPIView.as_view()),
    path('product/', views.ProductAPIView.as_view()),
    path('product/<int:pk>/', views.ProductAPIView.as_view()),
    path('product-variant/', views.ProductVariantAPIView.as_view()),
    path('product-variant/<int:pk>/', views.ProductVariantAPIView.as_view())
]
