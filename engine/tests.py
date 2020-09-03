from django.test import TestCase
from graph.models import DataNode, DataNodeType, DataEdge
from engine.forms import ComponentForm


class MockRequestResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class CommonTestCase:
    class ComponentTestCase(TestCase):
        node_name = ''
        node_type = None
        node_chart_type = None
        node_params = {}
        form_class = None

        @property
        def basic_form_fields(self):
            return {
                'title': 'New Test Node',
                'type': self.node.type,
                'name': self.node.name,
            }

        @property
        def special_form_fields(self):
            return {}

        def setUp(self):
            self.node = DataNode(
                title='Test Node',
                type=self.node_type,
                name=self.node_name,
                params=self.node_params
            )

        def test_form_load_from_node(self):
            form = self.form_class.load_from_node(self.node)
            self.assertBasicFormFields(form)
            self.assertSpecialFormFields(form)

        def test_form_save_to_node(self):
            self.node.delete()

            form_fields = self.basic_form_fields
            form_fields.update(self.special_form_fields)
            form = self.form_class(form_fields)
            node_id = form.save_to_node()
            node = DataNode.objects.get(id=node_id)

            self.assertBasicFields(node)
            self.assertSpecialFields(node)

        def assertBasicFormFields(self, form: ComponentForm):
            self.assertEqual(form.data['title'], self.node.title)
            self.assertEqual(form.data['type'], self.node.type)
            self.assertEqual(form.data['name'], self.node.name)

        def assertSpecialFormFields(self, form):
            pass

        def assertBasicFields(self, node: DataNode):
            self.assertEqual(node.title, 'New Test Node')
            self.assertEqual(node.name, self.node.name)
            self.assertEqual(node.type, self.node.type)

        def assertSpecialFields(self, node):
            pass

    class CalculatorTestCase(ComponentTestCase):
        @property
        def basic_form_fields(self):
            form_fields = super().basic_form_fields
            form_fields.update(dict(source_node=self.source))
            return form_fields

        def setUp(self):
            super().setUp()
            self.node.save()

            self.source = DataNode(
                title='Test Node Source',
                type=DataNodeType.READER,
                name='manual',
                params={
                    'columns': ['A', 'B'],
                    'data': [
                        {'0': 'ABC', '1': 'DEF'},
                        {'0': 'HIL', '1': 'KLM'}]
                }
            )
            self.source.save()

            self.data_edge = DataEdge(
                source=self.source,
                dest=self.node)
            self.data_edge.save()
