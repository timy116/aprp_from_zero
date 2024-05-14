from django.shortcuts import render


def login_view(request):
    template = 'login.html'

    return render(request, template, {})
