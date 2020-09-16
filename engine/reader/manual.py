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

    def process(self) -> DataFrame:
        # The first column is always considered as datetime and used as index
        data_list = {}
        for row in self.data:
            data_list[row[0]] = [d if d else np.nan for d in row[1:]]
        data_frame = DataFrame.from_dict(
            data_list, orient='index', columns=self.columns[1:])
        data_frame.index = pd.to_datetime(data_frame.index)
        return data_frame


class Form(ComponentForm):
    data = forms.CharField(
        label='Data', widget=Spreadsheet())

    @staticmethod
    def load_special_fields(node: DataNode):
        result = ComponentForm.load_special_fields(node)
        result.update({
            'data': json.dumps(node.params)
        })
        return result

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        node.params = json.loads(self.data['data'])
        node.save()
