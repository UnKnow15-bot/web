# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
 
    async def connect(self):
        print("✅ WebSocket connected!")
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Optional

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        print(message)
        # Echo the message back
        await self.send(text_data=json.dumps({
            'message': f"Server receiveds: {message}"
        }))
