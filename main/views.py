from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, "main/index.html", {"title": "Chat App"})


def error404(request, exception):
    return render(request, "main/404.html")


def error500(request):
    return render(request, "main/500.html")
