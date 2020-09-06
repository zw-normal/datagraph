from django.shortcuts import render


def index(request):
    return render(request, 'viewer/index.html', {'active_menu': 'home'})


def browser(request):
    return render(request, 'viewer/browser.html', {'active_menu': 'browser'})
