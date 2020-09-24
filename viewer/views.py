from django.shortcuts import render

from viewer.forms import VegaSpecNodesForm
from engine.queries import get_charts_count, get_data_nodes_count

def index(request):
    return render(request, 'viewer/index.html', {
        'active_menu': 'home',
        'charts_count': get_charts_count(),
        'data_notes_count': get_data_nodes_count(),
    })


def browser(request):
    form = VegaSpecNodesForm()

    return render(request, 'viewer/browser.html', {
        'active_menu': 'browser',
        'form': form
    })
