from pandas import DataFrame
from django import forms
from engine.component import Component
from engine.forms import CalculatorForm
from graph.models import DataNode


class Calculator(Component):

    def process(self) -> DataFrame:
        axis = getattr(self, 'axis', 'index')
        how = getattr(self, 'how', 'any')

        data_frame = self.process_source()
        if data_frame is not None:
            return data_frame.dropna(
                axis=axis, how=how, inplace=False)


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
        widget=forms.Select(attrs={'class': 'form-control'}))
    how = forms.ChoiceField(
        label='How', choices=HOW_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

    @staticmethod
    def load_special_fields(node: DataNode):
        result = CalculatorForm.load_special_fields(node)
        result.update({
            'axis': node.params.get('axis', 'index') if node.params else 'index',
            'how': node.params.get('how', 'any') if node.params else 'any'
        })
        return result

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'axis': self.data.get('axis', 'index'),
            'how': self.data.get('how', 'any')
        }
        node.save()
