from django import forms

from engine.component import Component
from engine.forms import CalculatorForm
from graph.models import DataNode


class Calculator(Component):

    def process(self):
        data_frame = self.process_source()

        multiplier = getattr(self, 'multiplier', 1.0)
        return data_frame.mul(multiplier)


class Form(CalculatorForm):

    multiplier = forms.FloatField(
        label='Multiplier',
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'multiplier': node.params.get('multiplier', 1.0) if node.params else 1.0
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'multiplier': self.cleaned_data['multiplier']
        }
        node.save()
