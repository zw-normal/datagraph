import uuid
import networkx as nx
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError


class DataNodeType(models.TextChoices):
    READER = 'READER', 'Reader'
    CALCULATOR = 'CALCULATOR', 'Calculator'
    AGGREGATOR = 'AGGREGATOR', 'Aggregator'
    WRITER = 'WRITER', 'Writer'


class Unit(models.Model):
    name = models.CharField(primary_key=True, max_length=128)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ('name',)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name == other.name)

    def __hash__(self):
        return hash(self.name)


class DataNode(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=128)
    name = models.CharField(
        max_length=128, db_index=True)
    type = models.CharField(
        max_length=20, choices=DataNodeType.choices, db_index=True)
    params = JSONField(
        null=True, blank=True)
    unit = models.ForeignKey(
        Unit, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Data Node'
        verbose_name_plural = 'Data Nodes'
        ordering = ('title',)

    def __str__(self):
        return '{title} ({id})'.format(title=self.title, id=self.id)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.id == other.id)

    def __hash__(self):
        return hash(self.id)


class DataEdge(models.Model):
    source = models.ForeignKey(
        DataNode, on_delete=models.CASCADE, related_name='source_nodes')
    dest = models.ForeignKey(
        DataNode, on_delete=models.CASCADE, related_name='dest_nodes')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.source.type == DataNodeType.WRITER:
            raise ValidationError(
                'WRITER node cannot be source node.')
        if self.dest.type == DataNodeType.CALCULATOR and \
                DataEdge.objects.filter(dest=self.dest).exists():
            raise ValidationError(
                'CALCULATOR node cannot be destination for multiple nodes.')
        if self.dest.type == DataNodeType.READER:
            raise ValidationError(
                'READER node cannot be destination node.')

        # Validate new link won't cause cyclic link
        graph = nx.DiGraph()
        graph.add_nodes_from(DataNode.objects.all())
        for edge in DataEdge.objects.all():
            graph.add_edge(edge.source, edge.dest)
        graph.add_edge(self.source, self.dest)
        if len(list(nx.simple_cycles(graph))) > 0:
            raise ValidationError(
                'The link is not achievable as causing cyclic links in graph')

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.source.id == other.source.id and
                self.dest.id == other.dest.id)

    def __hash__(self):
        return hash((self.source.id, self.dest.id))

    class Meta:
        verbose_name = 'Data Edge'
        verbose_name_plural = 'Data Edges'
        unique_together = ['source', 'dest']
