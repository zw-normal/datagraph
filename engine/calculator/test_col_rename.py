from graph.models import DataNodeType
from engine.calculator.col_rename import Form as ColumnRenameForm
from engine.tests import CommonTestCase


class ColumnRenameTestCase(CommonTestCase.CalculatorTestCase):
    node_name = 'col_rename'
    node_type = DataNodeType.CALCULATOR
    node_params = {
        'columns': ['A', 'B'],
        'new_names': ['D', 'E']
    }
    form_class = ColumnRenameForm

    @property
    def special_form_fields(self):
        return {
            'columns': ', '.join(self.node_params['columns']),
            'new_names': ', '.join(self.node_params['new_names'])
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(
            form.data['columns'], ', '.join(self.node.params['columns']))
        self.assertEqual(
            form.data['new_names'], ', '.join(self.node.params['new_names']))

    def assertSpecialFields(self, node):
        self.assertListEqual(
            node.params['columns'], self.node.params['columns'])
        self.assertListEqual(
            node.params['new_names'], self.node.params['new_names'])

    def assertProcess(self, result):
        columns = list(result.columns)
        self.assertListEqual(columns, ['D', 'E'])
