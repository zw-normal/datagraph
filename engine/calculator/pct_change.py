from pandas import DataFrame
from django import forms

from engine.component import Component
from engine.forms import CalculatorForm
from graph.models import DataNode


class Calculator(Component):

    def process(self):
        periods = getattr(self, 'periods', 1)

        data_frame = self.process_source()
        if data_frame is not None:
            return data_frame.sort_index().pct_change(periods=periods)
        return DataFrame()


class Form(CalculatorForm):

    periods = forms.IntegerField(
        label='Periods',
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'periods': node.params.get('periods', 1) if node.params else 1
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'periods': self.cleaned_data['periods']
        }
        node.save()
