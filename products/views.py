from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import ProductType, Product, ProductVariant
from .serializers import ProductTypeModelSerializer, ProductModelSerializer, ProductVariantModelSerializer

class ProductTypeAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        
        return [IsAdminUser()]

    def get(self, request, pk=None):
        if pk:
            product_type = get_object_or_404(ProductType, pk=pk)
            serializer = ProductTypeModelSerializer(product_type)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        product_types = ProductType.objects.all()
        serializer = ProductTypeModelSerializer(product_types, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductTypeModelSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk=None):
        product_type = get_object_or_404(ProductType, pk=pk)
        serializer = ProductTypeModelSerializer(product_type, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk=None):
        product_type = get_object_or_404(ProductType, pk=pk)
        serializer = ProductTypeModelSerializer(product_type, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        product_type = get_object_or_404(ProductType, pk=pk)

        product_type.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductAPIView(APIView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'product_type__name', 'description']
    filterset_fields = ['product_type__name']
    ordering_fields = ['name', 'price']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        
        return [IsAdminUser()]

    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductModelSerializer(product)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        products = Product.objects.all()
        queryset = self.filter_queryset(products)
        serializer = ProductModelSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductModelSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductModelSerializer(product, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductModelSerializer(product, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)

        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductVariantAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        
        return [IsAdminUser()]

    def get(self, request, pk=None):
        if pk:
            product_variant = get_object_or_404(ProductVariant, pk=pk)
            serializer = ProductVariantModelSerializer(product_variant)

            return Response(serializer.data, status=status.HTTP_200_OK)

        product_variants = ProductVariant.objects.all()
        serializer = ProductVariantModelSerializer(product_variants, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductVariantModelSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk=None):
        product_variant = get_object_or_404(ProductVariant, pk=pk)
        serializer = ProductVariantModelSerializer(product_variant, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk=None):
        product_variant = get_object_or_404(ProductVariant, pk=pk)
        serializer = ProductVariantModelSerializer(product_variant, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        product_variant = get_object_or_404(ProductVariant, pk=pk)

        product_variant.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
