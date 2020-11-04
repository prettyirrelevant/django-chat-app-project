from django import forms

from users.models import MyUser


class AddFriendForm(forms.Form):
    username = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_username(self):
        if not MyUser.objects.filter(
            username=self.cleaned_data.get("username")
        ).exists():
            raise forms.ValidationError("Username does not exist")

        if self.user.username == self.cleaned_data.get("username"):
            raise forms.ValidationError("You cannot add yourself")

        return self.cleaned_data.get("username")
