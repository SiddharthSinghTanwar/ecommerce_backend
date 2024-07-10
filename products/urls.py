
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, product_sold_count_view, echo_test_view

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sold-counts/', product_sold_count_view, name='product_sold_counts'),
    path('echo-test/', echo_test_view, name='echo_test'),

]