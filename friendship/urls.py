from django.urls import path
from friendship import views


app_name = "friendship"
urlpatterns = [
    path("friends/", views.friends, name="friendship"),
    path("<str:username>/accept", views.accept_request, name="accept-request"),
    path("<str:username>/reject", views.reject_request, name="reject-request"),
]