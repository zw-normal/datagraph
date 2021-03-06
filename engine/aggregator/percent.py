from django import forms
from django.core.exceptions import ValidationError

from engine.component import Component
from engine.forms import AggregatorForm
from graph.models import DataNode


class Aggregator(Component):

    def process(self):
        data_frames = self.process_source()
        assert len(data_frames) == 2

        # By default, the data_frames returned is ordered by data node id asc
        reverse = getattr(self, 'reverse', False)

        divisor = data_frames[0]
        dividend = data_frames[1]
        if reverse:
            divisor, dividend = dividend, divisor
        return divisor.div(dividend.iloc[:, 0], axis='index')*100


class Form(AggregatorForm):

    reverse = forms.BooleanField(label='Reverse', required=False)

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'reverse': node.params.get('reverse', False) if node.params else False
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'reverse': self.cleaned_data['reverse']
        }
        node.save()

    def clean_source_nodes(self):
        source_nodes = self.cleaned_data['source_nodes']
        if len(source_nodes) != 2:
            raise ValidationError('Must select 2 source nodes')
        return source_nodes
