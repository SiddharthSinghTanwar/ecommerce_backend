
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items', 'total', 'created_at', 'updated_at']

    def get_total(self, obj):
        return sum(item.quantity * item.price for item in obj.items.all())
    
class OrderCreateSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField()
    )

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(user=user)
        
        for item_data in validated_data['items']:
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )
        
        return order
    
