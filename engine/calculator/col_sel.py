from pandas import DataFrame
from django import forms

from engine.component import Component
from engine.forms import CalculatorForm
from graph.models import DataNode


class Calculator(Component):

    def process(self):
        data_frame = self.process_source()
        if data_frame is not None:
            return data_frame[self.columns]
        return DataFrame()


class Form(CalculatorForm):

    columns = forms.CharField(
        label='Columns', max_length=1024,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    @staticmethod
    def load_special_fields(node: DataNode):
        result = CalculatorForm.load_special_fields(node)
        result.update({
            'columns': ', '.join(node.params['columns'])
        })
        return result

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'columns': [c.strip() for c in self.data['columns'].split(',')]
        }
        node.save()
