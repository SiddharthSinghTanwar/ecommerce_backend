
from celery import shared_task
from .models import Product

@shared_task
def bulk_create_products(products_data):
    products = [Product(**data) for data in products_data]
    Product.objects.bulk_create(products)
    return f"Created {len(products)} products"