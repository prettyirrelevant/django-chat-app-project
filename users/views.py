from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserCreationForm


# Create your views here.


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully")
            return redirect(reverse("users:login"))
    return render(
        request, "users/register.html", {"title": "Create Account", "form": form}
    )


@login_required
def profile(request):
    return render(
        request,
        "users/profile.html",
        {"title": "Profile", "avatar": request.user.avatar},
    )


class UserLoginView(LoginView, SuccessMessageMixin):
    template_name = "users/login.html"
    extra_context = {"title": "Log In"}
    redirect_authenticated_user = True
    success_message = "Logged In Successfully"


class UserLogoutView(LogoutView, SuccessMessageMixin):
    template_name = "users/logout.html"
    success_message = "Logged Out Successfully"
