from django.shortcuts import render

from viewer.forms import VegaSpecNodesForm

def index(request):
    return render(request, 'viewer/index.html', {'active_menu': 'home'})


def browser(request):
    form = VegaSpecNodesForm()

    return render(request, 'viewer/browser.html', {
        'active_menu': 'browser',
        'form': form
    })
