from typing import List

from django.db.models import Q

from graph.models import Unit, DataNode, DataEdge, DataNodeType


def get_units():
    return Unit.objects.all()


def get_data_readers():
    return DataNode.objects.filter(type=DataNodeType.READER)


def get_data_nodes_by_ids(ids: [str]):
    return DataNode.objects.filter(id__in=ids)


def get_data_nodes_by_dest(id_: str):
    edges = DataEdge.objects.filter(dest_id=id_)
    return [edge.source for edge in edges]


def link_data_nodes(source: DataNode, dest: DataNode):
    if dest.type != DataNodeType.AGGREGATOR:
        DataEdge.objects.filter(dest=dest).delete()
    DataEdge.objects.get_or_create(
        source=source,
        dest=dest
    )


def set_data_node_sources(
        source_nodes: List[DataNode], node: DataNode):
    # Delete any existing nodes that is not in source_nodes
    DataEdge.objects.filter(
        ~Q(source__in=source_nodes) and Q(dest=node)).delete()

    for source_node in source_nodes:
        link_data_nodes(source_node, node)
