from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, reverse

from .forms import AddFriendForm
from .models import Friendship
from users.models import MyUser


@login_required
def friends(request):
    form = AddFriendForm(user=request.user)
    if request.method == "POST":
        form = AddFriendForm(request.POST, user=request.user)
        if form.is_valid():
            new_friend = MyUser.objects.get(username=form.cleaned_data.get("username"))
            current_user = request.user

            # checks if there is a pending request yet to be accepted.
            if (
                Friendship.objects.filter(user=new_friend, friend=current_user).count()
                > 0
            ):
                messages.warning(
                    request,
                    "You have a pending request or already rejected a request from this user",
                )
                return redirect(reverse("friendship:friendship"))

            # checks if the two users are friends already
            if Friendship.objects.filter(
                Q(user=current_user, friend=new_friend, status=1)
                | Q(user=new_friend, friend=current_user, status=1)
            ):
                messages.info(request, "You are already friends with this user")
                return redirect(reverse("friendship:friendship"))

            if Friendship.objects.filter(
                user=current_user, friend=new_friend, status=0
            ):
                messages.info(request, "You already sent a friend request to this user")
                return redirect(reverse("friendship:friendship"))

            # a success message
            Friendship.objects.create(user=current_user, friend=new_friend)
            messages.success(request, "Friend request sent successfully")
            return redirect(reverse("friendship:friendship"))

    return render(
        request,
        "friendship/friends.html",
        {
            "form": form,
            "title": "Friends",
            "friends": Friendship.friends(request.user),
            "requests": Friendship.pending_requests(request.user),
        },
    )


@login_required
def accept_request(request, username):
    friend = MyUser.objects.get(username=username)
    if friend:
        is_friendship_exists = Friendship.objects.get(
            user=friend, friend=request.user, status=0
        )
        if is_friendship_exists:
            friendship = Friendship.objects.get(
                user=friend, friend=request.user, status=0
            )
            friendship.status = 1
            friendship.save()

            messages.success(request, "Friend request accepted")
            return redirect(reverse("friendship:friendship"))

        messages.warning(request, "There is no request from this user")
        return redirect(reverse("friendship:friendship"))

    messages.error(request, "No account with such username exists")
    return redirect(reverse("friendship:friendship"))


@login_required
def reject_request(request, username):
    friend = MyUser.objects.get(username=username)
    if friend:
        is_friendship_exists = Friendship.objects.get(
            user=friend, friend=request.user, status=0
        )
        if is_friendship_exists:
            friendship = Friendship.objects.get(
                user=friend, friend=request.user, status=0
            )
            friendship.status = 2
            friendship.save()

            messages.success(request, "Friend request rejected")
            return redirect(reverse("friendship:friendship"))

        messages.warning(request, "There is no request from this user")
        return redirect(reverse("friendship:friendship"))

    messages.error(request, "No account with such username exists")
    return redirect(reverse("friendship:friendship"))
