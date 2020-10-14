from django.shortcuts import render

from viewer.forms import VegaSpecNodesForm, VegaPublicSpecNodesForm
from engine.queries import get_charts_count
from graph.queries import get_data_nodes_count


def index(request):
    is_authenticated = request.user.is_authenticated
    return render(request, 'viewer/index.html', {
        'active_menu': 'home',
        'charts_count': get_charts_count(not is_authenticated),
        'data_notes_count': get_data_nodes_count(not is_authenticated),
    })


def browser(request):
    form = VegaSpecNodesForm() if request.user.is_authenticated else VegaPublicSpecNodesForm()

    return render(request, 'viewer/browser.html', {
        'active_menu': 'browser',
        'form': form
    })
