from django import forms

from engine.component import Component
from engine.forms import CalculatorForm
from graph.models import DataNode


class Calculator(Component):

    def process(self):
        data_frame = self.process_source()

        addend = getattr(self, 'addend', 0)
        return data_frame.add(addend)


class Form(CalculatorForm):

    addend = forms.FloatField(
        label='addend',
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'addend': node.params.get('addend', 0) if node.params else 0
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'addend': self.cleaned_data['addend']
        }
        node.save()
