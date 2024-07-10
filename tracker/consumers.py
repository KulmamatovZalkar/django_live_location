import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class LocationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            'location_group',
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'location_group',
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        latitude = text_data_json['latitude']
        longitude = text_data_json['longitude']

        self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude
        }))

    def location_message(self, event):
        latitude = event['latitude']
        longitude = event['longitude']

        self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude
        }))
