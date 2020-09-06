from graph.models import DataNode


def get_vega_spec_writers():
    return DataNode.objects.filter(name='vega_line')
