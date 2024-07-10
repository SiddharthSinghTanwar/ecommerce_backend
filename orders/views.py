from django.shortcuts import render


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from cart.models import Cart
from .tasks import send_order_confirmation_email

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            with transaction.atomic():
                order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Only admin can update orders"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.is_staff or order.user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response({"error": "You don't have permission to delete this order"}, status=status.HTTP_403_FORBIDDEN)