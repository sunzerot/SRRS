from django.shortcuts import render


def index(request):
    return render(request, 'home/main/main.html')