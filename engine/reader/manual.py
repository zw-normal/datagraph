import json
from pandas import DataFrame
from django import forms
from engine.component import Component
from engine.forms import ComponentForm
from engine.widgets import Spreadsheet
from graph.models import DataNode


class Reader(Component):

    def process(self) -> DataFrame:
        data_frame = DataFrame.from_dict(self.data)
        data_frame.columns = self.columns
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
