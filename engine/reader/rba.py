import pandas as pd
from pandas import DataFrame
from django import forms
from django.core.cache import cache
from engine.component import Component
from engine.forms import ComponentForm
from graph.models import DataNode


class Reader (Component):

    def process(self) -> DataFrame:
        cache_key = str(self.data_node.id)
        result = cache.get(cache_key)
        if result is None:
            xls_url = 'https://www.rba.gov.au/statistics/tables/xls/{}.xls'\
                .format(self.category)
            result = pd.read_excel(
                xls_url, skiprows=10, index_col=0, sheet_name='Data')
            result = result.set_index(
                pd.to_datetime(result.index)).sort_index()
            cache.set(cache_key, result)
        return result


class Form(ComponentForm):
    category = forms.CharField(
        label='Category', max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    @staticmethod
    def load_special_fields(node: DataNode):
        result = ComponentForm.load_special_fields(node)
        result.update({
            'category': node.params['category']
        })
        return result

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {'category': self.data['category']}
        node.save()
