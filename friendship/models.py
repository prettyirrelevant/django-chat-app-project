from django.db import models

from users.models import MyUser


# Create your models here.


class Friendship(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="sender")
    friend = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="receiver"
    )
    status = models.PositiveSmallIntegerField(
        verbose_name="friendship status",
        default=0,
        help_text="0: Pending, 1: Accepted, 2: Rejected",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friendship_{self.user.username}_{self.friend.username}"

    @staticmethod
    def friends(user):
        friends = []
        for _ in Friendship.objects.filter(user=user, status=1):
            friends.append({"username": _.friend.username, "gravatar": _.friend.avatar})
        for _ in Friendship.objects.filter(friend=user, status=1):
            friends.append({"username": _.user.username, "gravatar": _.user.avatar})

        return friends

    @staticmethod
    def pending_requests(user):
        requests = []
        for _ in Friendship.objects.filter(friend=user, status=0):
            requests.append({"username": _.user.username, "gravatar": _.user.avatar})

        return requests
