from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, reverse, render

from friendship.models import Friendship
from users.models import MyUser
from .models import Conversation


# Create your views here.


@login_required
def start_conversation(request, username):
    participant = MyUser.objects.get(username=username)

    # Checks if the user exists or not
    if participant:
        friendship = Friendship.objects.filter(
            Q(user=request.user, friend=participant, status=1)
            | Q(user=participant, friend=request.user, status=1)
        )

        # checks if the logged in user and requested user are friends
        if friendship.exists():
            _conversation = Conversation.objects.filter(
                Q(initiator=request.user, receiver=participant)
                | Q(initiator=participant, receiver=request.user)
            )

            #  checks if a conversation has already begun
            if not _conversation.exists():
                new_convo = Conversation.objects.create(
                    initiator=request.user, receiver=participant
                )
                return redirect(reverse("chat:conversation", args=(new_convo.id,)))

            # redirects to the conversation that already exists
            return redirect(reverse("chat:conversation", args=(_conversation[0].id,)))

        # displays a message that the two users are not friends
        messages.warning(
            request, "Action cannot be completed because you are not friends"
        )
        return redirect(reverse("friendship:friendship"))

    # user doesn't exist
    messages.error(request, "User does not exist")
    return redirect(reverse("friendship:friendship"))


@login_required
def conversation(request, conversation_id):
    convo = Conversation.objects.filter(id=conversation_id)
    if not convo.exists():
        messages.warning(request, "Conversation does not exist")
        return redirect(reverse("friendship:friendship"))
    return render(
        request, "chat/room.html", {"conversation": convo[0], "title": "Conversation"}
    )


@login_required
def conversations(request):
    convo = (
        Conversation.objects.filter(
            Q(initiator=request.user) | Q(receiver=request.user)
        )
        .annotate(last_message_sent=Coalesce(Max("message__timestamp"), "timestamp"))
        .order_by("-last_message_sent")
    )
    return render(
        request, "chat/chat.html", {"conversations": convo, "title": "Conversations"}
    )
