from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path("message/<str:username>/", views.start_conversation, name="start-convo"),
    path(
        "conversation/<int:conversation_id>/", views.conversation, name="conversation"
    ),
    path("conversations/", views.conversations, name="conversations"),
]
