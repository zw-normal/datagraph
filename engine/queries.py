from django.db.models import Q

from graph.models import DataNode


def get_vega_spec_writers():
    return DataNode.objects.filter(
        Q(name='vega_line') | 
        Q(name='vega_stacked_area') |
        Q(name='vega_norm_stacked_area'))
