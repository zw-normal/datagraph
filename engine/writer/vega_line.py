import json

from django.template import loader

from engine.forms import WriterForm
from engine.component import Component


class Writer(Component):

    def process(self) -> str:
        data_frame = self.process_source()
        data_dict = data_frame.to_dict('split')

        data_result = []
        for row_count, row_index in enumerate(data_dict['index']):
            for column_count, column_index in enumerate(data_dict['columns']):
                data_result.append({
                    'x': row_index.timestamp() * 1000,
                    'y': data_dict['data'][row_count][column_count],
                    'c': column_index})

        tpl = loader.get_template('engine/vega_line_chart_spec.jinja2')
        return tpl.render(context={
            'title': self.title,
            'unit': self.unit.name,
            'data': json.dumps(data_result)
        })


class Form(WriterForm):
    pass