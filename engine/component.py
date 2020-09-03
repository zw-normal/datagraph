import importlib
from typing import List, Set
from abc import ABC, abstractmethod
from pandas import DataFrame
from django.db.models import Q
from graph.models import DataNode, DataEdge, DataNodeType


class Component(ABC):
    def __init__(self, data_node: DataNode):
        self.data_node = data_node

    def __getattr__(self, attr):
        if (self.data_node.params is not None) and \
                (attr in self.data_node.params):
            return self.data_node.params[attr]
        return getattr(self.data_node, attr)

    @classmethod
    def graph(cls, nodes: List[DataNode]) -> Set[DataEdge]:
        edges = set()
        node_ids_marked = set()
        for node in nodes:
            cls._get_graph(node, node_ids_marked, edges)
        return edges

    @classmethod
    def _get_graph(
            cls,
            node: DataNode,
            node_ids_marked: Set[DataNode],
            edges: Set[DataEdge]):
        if node.id in node_ids_marked:
            return

        node_ids_marked.add(node.id)
        for edge in DataEdge.objects.filter(
                Q(source__id=node.id) | Q(dest__id=node.id)):
            edges.add(edge)
            cls._get_graph(edge.source, node_ids_marked, edges)
            cls._get_graph(edge.dest, node_ids_marked, edges)

    @abstractmethod
    def process(self) -> DataFrame:
        raise NotImplementedError

    def process_source(self):
        if self.data_node.type == DataNodeType.AGGREGATOR:
            data_frames = []
            edges = DataEdge.objects.filter(
                dest__id=self.data_node.id)
            for edge in edges:
                data_frames.append(
                    self.get_component(edge.source).process())
            return data_frames
        edge = DataEdge.objects.get(dest__id=self.data_node.id)
        return self.get_component(edge.source).process()

    @classmethod
    def get_component(cls, node: DataNode):
        module = cls._load_module(node)
        class_name = node.type.lower().capitalize()
        return getattr(module, class_name)(node)

    @classmethod
    def get_form_class(cls, node: DataNode):
        module = cls._load_module(node)
        return getattr(module, 'Form')

    @staticmethod
    def _load_module(node: DataNode):
        module_name = 'engine.{type}.{name}'.format(
            type=node.type.lower(),
            name=node.name)
        return importlib.import_module(module_name)

    @classmethod
    def json_data(cls, node: DataNode):
        return cls.get_component(node).process()
