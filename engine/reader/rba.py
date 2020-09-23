import pandas as pd
from django import forms

from engine.component import Component
from engine.forms import ComponentForm
from graph.models import DataNode


class Reader (Component):

    @Component.with_cache
    def process(self):
        skip_rows = getattr(self, 'skip_rows', 10)

        xls_url = 'https://www.rba.gov.au/statistics/tables/xls/{}.xls'\
            .format(self.category)
        result = pd.read_excel(
            xls_url, skiprows=skip_rows, index_col=0, sheet_name='Data')
        result = result.set_index(
            pd.to_datetime(result.index)).sort_index()
        return result


class Form(ComponentForm):
    category = forms.CharField(
        label='Category', max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    skip_rows = forms.IntegerField(
        label='Skip Rows',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'category': node.params['category'],
            'skip_rows': node.params.get('skip_rows', 10)
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'category': self.cleaned_data['category'],
            'skip_rows': self.cleaned_data['skip_rows']
        }
        node.save()
