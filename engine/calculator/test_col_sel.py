from graph.models import DataNodeType
from engine.calculator.col_sel import Form as ColumnSelectionForm
from engine.tests import CommonTestCase


class ColumnSelectionTestCase(CommonTestCase.CalculatorTestCase):
    node_name = 'col_sel'
    node_type = DataNodeType.CALCULATOR
    node_params = {
        'columns': ['A'],
    }
    form_class = ColumnSelectionForm

    @property
    def special_form_fields(self):
        return {
            'columns': ', '.join(self.node_params['columns']),
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(
            form.data['columns'], ', '.join(self.node.params['columns']))

    def assertSpecialFields(self, node):
        self.assertListEqual(
            node.params['columns'], self.node.params['columns'])

    def assertProcess(self, result):
        columns = list(result.columns)
        self.assertListEqual(columns, ['A'])
