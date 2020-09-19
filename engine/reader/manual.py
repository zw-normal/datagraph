import json
import numpy as np
import pandas as pd

from pandas import DataFrame
from django import forms

from engine.component import Component
from engine.forms import ComponentForm
from engine.widgets import Spreadsheet
from graph.models import DataNode


class Reader(Component):

    def process(self):
        # The first column is always used as index
        data_list = {}
        is_time_series = getattr(self, 'is_time_series', True)
        for row in self.raw_data.get('data', []):
            row_index = row[0]
            if is_time_series:
                row_index = pd.to_datetime(row_index, errors='ignore')
            data_list[row_index] = [d if d else np.nan for d in row[1:]]
        data_frame = DataFrame.from_dict(
            data_list,
            orient='index',
            columns=self.raw_data.get('columns', [])[1:])
        return data_frame


class Form(ComponentForm):
    raw_data = forms.CharField(
        label='Data', widget=Spreadsheet())
    is_time_series = forms.BooleanField(
        label='Time Series', initial=True)

    @staticmethod
    def load_special_fields(node: DataNode):
        result = ComponentForm.load_special_fields(node)
        result.update({
            'raw_data': json.dumps(node.params.get('raw_data', [])),
            'is_time_series': node.params.get('is_time_series', True)
        })
        return result

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = {
            'raw_data': json.loads(self.data.get('raw_data', [])),
            'is_time_series': self.data.get('is_time_series', True)}
        node.save()
