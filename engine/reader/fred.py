from datetime import datetime

import pandas_datareader as pdr
from django import forms

from engine.component import Component
from engine.forms import ComponentForm
from graph.models import DataNode


class Reader (Component):

    @Component.with_cache
    def process(self):
        symbol = getattr(self, 'symbol')
        return pdr.get_data_fred(
            symbol, start=datetime(1900, 1, 1))

class Form(ComponentForm):
    symbol = forms.CharField(
        label='Symbol', max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'symbol': node.params['symbol']
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'symbol': self.cleaned_data['symbol']
        }
        node.save()
