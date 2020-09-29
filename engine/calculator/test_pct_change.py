from graph.models import DataNodeType
from engine.calculator.pct_change import Form as PercentChangeForm
from engine.tests import CommonTestCase


class PercentChangeTestCase(CommonTestCase.CalculatorTestCase):
    node_name = 'pct_change'
    node_type = DataNodeType.CALCULATOR
    node_params = {
        'periods': 1
    }
    form_class = PercentChangeForm

    def assertProcess(self, result):
        self.assertEqual(2.0, result.iloc[1, 0])

    @property
    def special_form_fields(self):
        return {
            'periods': 1,
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(
            form.data['periods'], 1)

    def assertSpecialFields(self, node):
        self.assertDictEqual(node.params, self.node.params)
