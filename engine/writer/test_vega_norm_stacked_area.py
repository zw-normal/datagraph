from graph.models import DataNodeType
from engine.writer.vega_norm_stacked_area import Form as VegaNormalStackedAreaForm
from engine.tests import CommonTestCase


class VegaLineTestCase(CommonTestCase.WriterTestCase):
    node_name = 'vega_norm_stacked_area'
    node_type = DataNodeType.WRITER
    node_params = {
        'column_titles': [
            {'column': 'A', 'title': 'Title A'},
            {'column': 'B', 'title': 'Title B'},
        ]
    }
    form_class = VegaNormalStackedAreaForm

    @property
    def special_form_fields(self):
        return {
            'column_titles': 'A::Title A, B::Title B'
        }

    def assertSpecialFormFields(self, form):
        self.assertEqual(form.data['column_titles'], 'A::Title A, B::Title B')

    def assertSpecialFields(self, node):
        self.assertDictEqual(node.params, self.node.params)

    def assertProcess(self, result):
        self.assertTrue(
            'Vega lite nominal stacked area chart specification.' in result)
