from django.db import models

from users.models import MyUser


# Create your models here.


class Conversation(models.Model):
    initiator = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="convo_starter"
    )
    receiver = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="convo_participant"
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(
        MyUser, on_delete=models.PROTECT, related_name="message_sender"
    )
    receiver = models.ForeignKey(
        MyUser, on_delete=models.PROTECT, related_name="message_receiver"
    )
    text = models.CharField(max_length=200)
    attachment = models.ImageField(blank=True)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
