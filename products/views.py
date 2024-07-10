from django.shortcuts import render


from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer, BulkUploadSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import bulk_create_products
from celery.result import AsyncResult

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def bulk_upload(self, request):
        products_data = request.data.get('products', [])
        if not products_data:
            return Response({"error": "No products data provided"}, status=400)
        
        task = bulk_create_products.delay(products_data)
        return Response({"message": "Bulk upload task started", "task_id": task.id}, status=202)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def scheduled_tasks(self, request):
        task_id = request.query_params.get('task_id')
        if task_id:
            task = AsyncResult(task_id)
            return Response({
                "task_id": task_id,
                "status": task.status,
                "result": task.result
            })
        else:
            # In a real-world scenario, you'd implement a way to list all scheduled tasks
            return Response({"error": "Please provide a task_id"}, status=400)
        
def product_sold_count_view(request):
    return render(request, 'product_sold_count.html')

def echo_test_view(request):
    return render(request, 'echo_test.html')

