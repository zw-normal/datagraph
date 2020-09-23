from django import forms

from engine.component import Component
from engine.forms import AggregatorForm
from graph.models import DataNode


class Aggregator(Component):

    def process(self):
        # By default, the data_frames returned is ordered by data node id asc
        reverse = getattr(self, 'reverse', False)

        data_frames = self.process_source()
        assert len(data_frames) == 2

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
