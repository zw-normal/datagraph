from django.db.models import Q

from graph.models import DataNode, DataEdge


def get_vega_spec_writers():
    return DataNode.objects.filter(
        Q(name='vega_line') |
        Q(name='vega_stacked_area') |
        Q(name='vega_norm_stacked_area'))


def is_node_deletable(node_id: str):
    return not DataEdge.objects.filter(source__id=node_id).exists()
