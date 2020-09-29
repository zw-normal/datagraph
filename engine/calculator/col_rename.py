from pandas import DataFrame
from django import forms

from engine.component import Component
from engine.forms import CalculatorForm
from graph.models import DataNode


class Calculator(Component):

    def process(self):
        data_frame = self.process_source()
        rename_dict = dict(zip(self.columns, self.new_names))
        if data_frame is not None:
            return data_frame.rename(columns=rename_dict)
        return DataFrame()


class Form(CalculatorForm):
    columns = forms.CharField(
        label='Original Columns', max_length=1024,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_names = forms.CharField(
        label='New Names', max_length=1024,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'columns': ', '.join(node.params['columns']),
            'new_names': ', '.join(node.params['new_names'])
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'columns': [c.strip() for c in self.cleaned_data['columns'].split(',')],
            'new_names': [c.strip() for c in self.cleaned_data['new_names'].split(',')]
        }
        node.save()
