from datetime import datetime

from graph.models import DataNodeType
from engine.writer.vega_line import Form as VegaLineForm
from engine.tests import CommonTestCase


class VegaLineTestCase(CommonTestCase.WriterTestCase):
    node_name = 'vega_line'
    node_type = DataNodeType.WRITER
    node_params = {
        'column_titles': [
            {'column': 'A', 'title': 'Title A'},
            {'column': 'B', 'title': 'Title B'},
        ]
    }
    source_node_params = {
        'columns': ['A', 'B'],
        'data': [
            {'2015-05-17': 100.0, '2015-06-17': 200.0},
            {'2015-05-17': 300.0, '2015-06-17': 400.0}]
    }
    form_class = VegaLineForm

    @property
    def special_form_fields(self):
        return {
            'column_titles': 'A::Title A, B::Title B'
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(form.data['column_titles'], 'A::Title A, B::Title B')

    def assertSpecialFields(self, node):
        self.assertDictEqual(node.params, self.node.params)
