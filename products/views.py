from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from .models import ProductType, Product
from .serializers import ProductTypeModelSerializer, ProductModelSerializer

class ProductTypeModelViewSet(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeModelSerializer
    permission_classes = [IsAdminUser]

class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'product_type', 'is_active']
    search_fields = ['name', 'description', 'category', 'product_type__name']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('images').order_by('-created_at')

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        
        return [IsAdminUser()]
    