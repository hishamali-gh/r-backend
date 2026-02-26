from django.urls import path
from . import views

urlpatterns = [
    path('product-types/', views.ProductTypeAPIView.as_view()),
    path('product-types/<int:pk>/', views.ProductTypeAPIView.as_view()),
    path('products/', views.ProductAPIView.as_view()),
    path('products/<int:pk>/', views.ProductAPIView.as_view()),
    path('product-variants/', views.ProductVariantAPIView.as_view()),
    path('product-variants/<int:pk>/', views.ProductVariantAPIView.as_view()),
    path('products/<int:product_id>/images/', views.ProductImageAPIView.as_view()),
    path('products/<int:product_id>/images/<int:image_id>/', views.ProductImageAPIView.as_view())
]
