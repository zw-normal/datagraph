import json

import pandas as pd

from pandas import DataFrame
from django import forms

from engine.component import Component
from engine.forms import ComponentForm
from engine.widgets import Spreadsheet
from engine.convertor import to_float
from graph.models import DataNode


class Reader(Component):

    def process(self):
        # The first column is always used as index
        data_list = {}
        is_time_series = getattr(self, 'is_time_series', True)
        to_month_end = getattr(self, 'to_month_end', False)
        for row in self.raw_data.get('data', []):
            row_index = row[0]
            if is_time_series:
                if to_month_end:
                    row_index = pd.to_datetime(row_index, errors='ignore') + pd.offsets.MonthEnd()
                else:
                    row_index = pd.to_datetime(row_index, errors='ignore')
            data_list[row_index] = [to_float(d) for d in row[1:]]
        data_frame = DataFrame.from_dict(
            data_list,
            orient='index',
            columns=self.raw_data.get('columns', [])[1:])
        return data_frame


class Form(ComponentForm):
    raw_data = forms.CharField(
        label='Data', widget=Spreadsheet())
    is_time_series = forms.BooleanField(
        label='Time Series', initial=True, required=False)
    to_month_end = forms.BooleanField(
        label='Month End', initial=False, required=False)

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'raw_data': json.dumps(node.params.get('raw_data', [])),
            'is_time_series': node.params.get('is_time_series', True),
            'to_month_end': node.params.get('to_month_end', False)
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'raw_data': json.loads(self.cleaned_data['raw_data']),
            'is_time_series': self.cleaned_data['is_time_series'],
            'to_month_end': self.cleaned_data['to_month_end']
        }
        node.save()
