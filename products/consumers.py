
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Product

class ProductSoldCountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("product_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("product_updates", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        
        if action == 'get_sold_counts':
            sold_counts = await self.get_all_product_sold_counts()
            await self.send(text_data=json.dumps({
                'type': 'sold_counts',
                'data': sold_counts
            }))

    async def product_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'product_update',
            'product_id': event['product_id'],
            'sold_count': event['sold_count']
        }))

    @database_sync_to_async
    def get_all_product_sold_counts(self):
        return list(Product.objects.values('id', 'sold_count'))
    
class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': f"Echo: {message}"
        }))