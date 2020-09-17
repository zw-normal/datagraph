import importlib

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from graph.models import DataNode, DataNodeType
from graph.queries import get_data_nodes_by_ids
from engine.component import Component
from engine.forms import DataReadersForm
from engine.queries import is_node_deletable


@login_required
def workbench(request):
    node_ids = request.session.get('source_node_ids', set())
    if node_ids:
        source_nodes = get_data_nodes_by_ids(node_ids)
        form = DataReadersForm({'source_nodes': source_nodes})
    else:
        form = DataReadersForm()
    return render(
        request, 'engine/workbench.html',
        {
            'active_menu': 'workbench',
            'form': form
        })


@login_required
def new_node_editor(
        request,
        node_type: str,
        node_name: str,
        source_id: str = None):
    py_node_name = node_name.replace('-', '_')

    module_name = 'engine.{type}.{name}'.format(
        type=node_type,
        name=py_node_name)
    module = importlib.import_module(module_name)
    form_class = getattr(module, 'Form')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            node_id = form.save_to_node()
            if node_type == DataNodeType.READER.value.lower():
                request.session['source_nodes'] = request.session.get('source_nodes', set())
                request.session['source_nodes'].add(node_id)
            messages.success(request, 'Node has been saved.')
            return HttpResponseRedirect(reverse('engine:workbench'))
    else:
        form_fields = {
            'type': node_type.upper(),
            'name': py_node_name
        }
        if source_id:
            if node_type == 'aggregator':
                form_fields.update({
                    'source_nodes': [DataNode.objects.get(id=source_id)]
                })
            else:
                form_fields.update({
                    'source_node': DataNode.objects.get(id=source_id)
                })
        form = form_class(initial=form_fields)

    return render(
        request,
        'engine/node_editor.html',
        {
            'active_menu': 'workbench',
            'form': form
        }
    )


@login_required
def existing_node_editor(request, node_id: str):
    node = get_object_or_404(DataNode, id=node_id)
    form_class = Component.get_form_class(node)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save_to_node()
            messages.success(request, 'Node has been saved.')
            return HttpResponseRedirect(reverse('engine:workbench'))
    else:
        form = form_class.load_from_node(node)

    return render(
        request,
        'engine/node_editor.html',
        {
            'active_menu': 'workbench',
            'node_id': node_id,
            'form': form
        }
    )


@login_required
def delete_node(request, node_id: str):
    node = get_object_or_404(DataNode, id=node_id)
    if is_node_deletable(node_id):
        node.delete()
        messages.success(request, 'Node has been deleted.')
        return HttpResponseRedirect(reverse('engine:workbench'))
    messages.error(request, 'Node cannot be deleted.')
    return HttpResponseRedirect(
        reverse('engine:existing-node-editor', kwargs={'node_id': node_id}))


def vega_spec(request, node_id: str):
    """This view generates vega visualization specification"""
    data_node = get_object_or_404(DataNode, id=node_id)
    data_component = Component.get_component(data_node)

    return HttpResponse(
        data_component.process(),
        content_type='application/json')
