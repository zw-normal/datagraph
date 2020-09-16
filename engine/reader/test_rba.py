import json

from graph.models import DataNodeType
from engine.reader.rba import \
    Reader as RbaReader, Form as RbaReaderForm
from engine.tests import CommonTestCase

class RbaReaderTestCase(CommonTestCase.ComponentTestCase):
    node_name = 'rba'
    node_type = DataNodeType.READER
    node_params = {
        'category': 'd02hist',
    }
    form_class = RbaReaderForm

    @property
    def special_form_fields(self):
        return {
            'category': 'd02hist'
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(form.data['category'], 'd02hist')

    def assertSpecialFields(self, node):
        self.assertDictEqual(node.params, self.node.params)

    def assertProcess(self, result):
        self.assertEqual(result.loc[:, 'DLCALAB'][0], 18.595)
