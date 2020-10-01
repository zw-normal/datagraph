from django import forms

from engine.forms import CalculatorForm
from graph.models import DataNode


class RollingForm(CalculatorForm):

    window = forms.IntegerField(
        label='Window',
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'window': node.params.get('window', 1) if node.params else 1
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'window': self.cleaned_data['window']
        }
        node.save()
