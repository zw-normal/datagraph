from django.db.models import Q

from graph.models import DataNode, DataEdge


def get_vega_spec_writers(public_only: bool = False):
    criteria = (Q(name='vega_line') |
                Q(name='vega_stacked_area') |
                Q(name='vega_norm_stacked_area'))
    if public_only:
        criteria = criteria & Q(public=True)
    return DataNode.objects.filter(criteria)


def get_charts_count(public_only: bool = False):
    return get_vega_spec_writers(public_only).count()


def is_node_deletable(node_id: str):
    return not DataEdge.objects.filter(source__id=node_id).exists()
