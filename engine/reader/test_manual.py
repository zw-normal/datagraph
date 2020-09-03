import json
from graph.models import DataNodeType
from engine.reader.manual import \
    Reader as ManualReader, Form as ManualReaderForm
from engine.tests import CommonTestCase


class ManualReaderTestCase(CommonTestCase.ComponentTestCase):
    node_name = 'manual'
    node_type = DataNodeType.READER
    node_params = {
        'columns': ['A', 'B'],
        'data': [
            {'0': 'ABC', '1': 'DEF'},
            {'0': 'HIL', '1': 'KLM'}]
    }
    form_class = ManualReaderForm

    @property
    def special_form_fields(self):
        return {
            'data': json.dumps(self.node_params)
        }

    def test_process(self):
        reader = ManualReader(self.node)
        data_frame = reader.process()
        self.assertListEqual(list(data_frame.columns), ['A', 'B'])
        self.assertListEqual(
            data_frame.iloc[0].tolist(), ['ABC', 'DEF'])
        self.assertListEqual(
            data_frame.iloc[1].tolist(), ['HIL', 'KLM'])
        self.assertListEqual(
            data_frame['A'].tolist(), ['ABC', 'HIL'])
        self.assertListEqual(
            data_frame['B'].tolist(), ['DEF', 'KLM'])

    def assertSpecialFormFields(self, form):
        self.assertEqual(form.data['data'], json.dumps(self.node.params))

    def assertSpecialFields(self, node):
        self.assertDictEqual(node.params, self.node.params)
