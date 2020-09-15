from graph.models import DataNodeType
from engine.calculator.mul import Form as MultiplicationForm
from engine.tests import CommonTestCase


class MultiplicationTestCase(CommonTestCase.CalculatorTestCase):
    node_name = 'mul'
    node_type = DataNodeType.CALCULATOR
    node_params = {
        'multiplier': 0.001,
    }
    form_class = MultiplicationForm

    @property
    def special_form_fields(self):
        return {
            'multiplier': 0.001,
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(
            form.data['multiplier'], 0.001)

    def assertSpecialFields(self, node):
        self.assertDictEqual(node.params, self.node.params)

    def assertProcess(self, result):
        self.assertEqual(0.1, result.loc[0, 'A'])
