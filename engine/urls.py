from django.urls import path
from . import views

app_name = 'engine'
urlpatterns = [
    path('', views.workbench, name='workbench'),
    path(
        'vega-spec/<uuid:node_id>/',
        views.vega_spec,
        name='vega-spec'),
    path(
        'node-editor/<uuid:node_id>/',
        views.existing_node_editor,
        name='existing-node-editor'),
    path(
        'node_editor/<slug:node_type>/<slug:node_name>/',
        views.new_node_editor,
        name='new-source-node-editor'),
    path(
        'node_editor/<slug:node_type>/<slug:node_name>/<uuid:source_id>',
        views.new_node_editor,
        name='new-node-editor'
    ),
    path(
        'node-editor/<uuid:node_id>/delete',
        views.delete_node,
        name='node-editor-deletion'
    )
]
