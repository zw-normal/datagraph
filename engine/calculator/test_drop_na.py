from graph.models import DataNodeType
from engine.calculator.drop_na import Form as DropNaForm
from engine.tests import CommonTestCase


class DropNaTestCase(CommonTestCase.CalculatorTestCase):
    node_name = 'drop_na'
    node_type = DataNodeType.CALCULATOR
    node_params = {
        'axis': 'columns',
        'how': 'all'
    }
    form_class = DropNaForm

    @property
    def special_form_fields(self):
        return {
            'axis': 'columns',
            'how': 'all'
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(form.data['axis'], 'columns')
        self.assertEqual(form.data['how'], 'all')

    def assertSpecialFields(self, node):
        self.assertDictEqual(node.params, self.node.params)
