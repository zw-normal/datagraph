from graph.models import DataNodeType
from engine.calculator.pct_change import Form as PercentChangeForm
from engine.tests import CommonTestCase


class PercentChangeTestCase(CommonTestCase.CalculatorTestCase):
    node_name = 'pct_change'
    node_type = DataNodeType.CALCULATOR
    node_params = {}
    form_class = PercentChangeForm

    def assertProcess(self, result):
        self.assertEqual(2.0, result.loc[1, 'A'])
