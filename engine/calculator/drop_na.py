from pandas import DataFrame
from django import forms

from engine.component import Component
from engine.forms import CalculatorForm
from graph.models import DataNode


class Calculator(Component):

    def process(self):
        axis = getattr(self, 'axis', 'index')
        how = getattr(self, 'how', 'any')

        data_frame = self.process_source()
        if data_frame is not None:
            return data_frame.dropna(
                axis=axis, how=how, inplace=False)
        return DataFrame()


class Form(CalculatorForm):
    AXIS_CHOICES = (
        ('index', 'index'),
        ('columns', 'columns'),
    )
    HOW_CHOICES = (
        ('any', 'any'),
        ('all', 'all')
    )

    axis = forms.ChoiceField(
        label='Axis', choices=AXIS_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-control selectpicker'}))
    how = forms.ChoiceField(
        label='How', choices=HOW_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-control selectpicker'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'axis': node.params.get('axis', 'index') if node.params else 'index',
            'how': node.params.get('how', 'any') if node.params else 'any'
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'axis': self.cleaned_data['axis'],
            'how': self.cleaned_data['how']
        }
        node.save()
