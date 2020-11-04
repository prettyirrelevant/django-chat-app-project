import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from users.models import MyUser
from .models import Message, Conversation


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        # unpack the dictionary into the necessary parts
        message, sender, receiver, time, attachment = (
            text_data_json["message"],
            text_data_json["sender"],
            text_data_json["recepient"],
            datetime.utcfromtimestamp(text_data_json["time"] / 1000.0),
            text_data_json.get("attachment"),
        )

        conversation = Conversation.objects.get(id=int(self.room_name))
        sender = MyUser.objects.get(username=sender)
        receiver = MyUser.objects.get(username=receiver)

        # Attachment
        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]

            # make i no lie, i don't know what happens here. later things
            file_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            _message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                timestamp=time,
                attachment=file_data,
                text=message,
                conversation_id=conversation,
            )
        else:
            _message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                timestamp=time,
                text=message,
                conversation_id=conversation,
            )
        # Send message to room group
        if _message.attachment:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender.username,
                    "attachment": _message.attachment.url,
                    "time": str(_message.timestamp),
                },
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender.username,
                    "time": str(_message.timestamp),
                },
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        if event.get("attachment"):
            self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "sender": event["sender"],
                        "time": event["time"],
                        "attachment": event["attachment"],
                    }
                )
            )
        else:
            self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "sender": event["sender"],
                        "time": event["time"],
                    }
                )
            )
