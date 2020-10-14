import graphene
from graphene_django.types import DjangoObjectType
from graphene.types import Scalar

from engine.component import Component
from graph.models import DataNode, DataEdge, Unit
from graph.queries import get_data_nodes_by_ids, get_data_node_by_id


class DataFrame(Scalar):
    @staticmethod
    def serialize(dt):
        return dt.to_json(orient='split', double_precision=2)


class UnitType(DjangoObjectType):
    class Meta:
        model = Unit


class ComponentType(DjangoObjectType):
    class Meta:
        model = DataNode

    data = graphene.Field(DataFrame)

    def resolve_data(self, info):
        return Component.get_component(self).process()


class DataEdgeType(DjangoObjectType):
    class Meta:
        model = DataEdge


class Query:
    units = graphene.List(UnitType)
    data_readers = graphene.List(ComponentType)
    data_node = graphene.Field(
        ComponentType, id=graphene.UUID())
    data_nodes = graphene.List(
        ComponentType, ids=graphene.List(graphene.UUID))
    data_edges = graphene.List(
        DataEdgeType, ids=graphene.List(graphene.UUID))

    def resolve_units(self, info, **kwargs):
        return Unit.objects.all()

    def resolve_data_node(self, info, **kwargs):
        node_id = kwargs.get('id')
        if node_id is not None:
            return get_data_node_by_id(
                node_id, not info.context.user.is_authenticated)
        return None

    def resolve_data_nodes(self, info, **kwargs):
        session = info.context.session
        if kwargs.get('ids'):
            ids = set(kwargs.get('ids'))
        else:
            ids = set()
        session['source_node_ids'] = ids
        if ids:
            return list(get_data_nodes_by_ids(
                ids, not info.context.user.is_authenticated))
        return []

    def resolve_data_edges(self, info, **kwargs):
        ids = set(kwargs.get('ids'))
        if ids:
            nodes = list(get_data_nodes_by_ids(
                ids, not info.context.user.is_authenticated))
            return Component.graph(nodes)
        return []
