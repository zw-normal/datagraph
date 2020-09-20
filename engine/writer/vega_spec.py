import json

from django.template import loader
from django import forms

from engine.forms import WriterForm
from engine.component import Component
from graph.models import DataNode


class Writer(Component):

    JINJA2_TEMPLATE_FILE = ''

    def process(self) -> str:
        data_frame = self.process_source()
        data_dict = data_frame.to_dict('split')

        data_result = []
        for row_count, row_index in enumerate(data_dict['index']):
            for column_count, column_index in enumerate(data_dict['columns']):
                data_result.append({
                    'x': int(row_index.timestamp() * 1000),
                    'y': data_dict['data'][row_count][column_count],
                    'c': self.get_column_title(column_index)})

        tpl = loader.get_template(
            'engine/{}'.format(self.JINJA2_TEMPLATE_FILE))
        return tpl.render(context={
            'title': self.title,
            'unit': self.unit.name if self.unit else '',
            'data': json.dumps(data_result)
        })

    def get_column_title(self, column):
        if self.data_node.params:
            column_titles = self.data_node.params.get('column_titles', [])
            for column_title in column_titles:
                if column_title['column'] == column:
                    return column_title['title']
        return column            


class Form(WriterForm):

    column_titles = forms.CharField(
        label='Column Titles', max_length=4096,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    @classmethod
    def load_special_fields(cls, node: DataNode):
        fields = super().load_special_fields(node)
        fields.update({
            'column_titles': ', '.join(
                ('{}::{}'.format(ct['column'], ct['title']) for ct in node.params.get('column_titles', [])))
        })
        return fields

    def save_special_fields(self, node: DataNode):
        super().save_special_fields(node)
        column_titles = []
        for column_title in self.data['column_titles'].split(','):
            column, title = tuple(ct.strip() for ct in column_title.strip().split('::'))
            column_titles.append({'column': column, 'title': title})
        node.params = {
            'column_titles': column_titles
        }
        node.save()
