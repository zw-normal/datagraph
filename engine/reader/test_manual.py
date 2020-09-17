import json

from graph.models import DataNodeType
from engine.reader.manual import Form as ManualReaderForm
from engine.tests import CommonTestCase


class ManualReaderTestCase(CommonTestCase.ComponentTestCase):
    node_name = 'manual'
    node_type = DataNodeType.READER
    node_params = {
        'raw_data': {
            'columns': ['D', 'A', 'B'],
            'data': [
                ['2015-05-17', 'ABC', 'DEF'],
                ['2015-06-17', 'HIL', 'KLM']
            ]},
        'is_time_series': True
    }
    form_class = ManualReaderForm

    @property
    def special_form_fields(self):
        return {
            'raw_data': json.dumps(self.node_params['raw_data']),
            'is_time_series': True
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(
            form.data['raw_data'],
            json.dumps(self.node.params['raw_data']))

    def assertSpecialFields(self, node):
        self.assertDictEqual(node.params, self.node.params)

    def assertProcess(self, result):
        self.assertListEqual(list(result.columns), ['A', 'B'])
        self.assertListEqual(
            result.iloc[0].tolist(), ['ABC', 'DEF'])
        self.assertListEqual(
            result.iloc[1].tolist(), ['HIL', 'KLM'])
        self.assertListEqual(
            result['A'].tolist(), ['ABC', 'HIL'])
        self.assertListEqual(
            result['B'].tolist(), ['DEF', 'KLM'])
