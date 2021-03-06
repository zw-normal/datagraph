from django.test import TestCase
from django.conf import settings

from graph.models import DataNode, DataNodeType, DataEdge
from graph.queries import get_data_node_by_id
from engine.forms import ComponentForm
from engine.component import Component


class CommonTestCase:

    class ComponentTestCase(TestCase):
        node_name = ''
        node_type = None
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
            node = get_data_node_by_id(node_id)

            self.assertBasicFields(node)
            self.assertSpecialFields(node)

        def test_process(self):
            if self.node_type != DataNodeType.READER or \
                    self.node_name not in settings.EXCLUDED_PROCESS_TEST_OF_READERS:
                result = Component.get_component(self.node).process()
                self.assertProcess(result)

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

        def assertProcess(self, result):
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
                    'raw_data': {
                        'columns': ['D', 'A', 'B'],
                        'data': [
                            ['2015-05-17', 100.0, ''],
                            ['2015-06-17', 300.0, '']
                        ]},
                    'is_time_series': True
                }
            )
            self.source.save()

            data_edge = DataEdge(
                source=self.source,
                dest=self.node)
            data_edge.save()

    class AggregatorTestCase(CalculatorTestCase):

        @property
        def basic_form_fields(self):
            form_fields = super().basic_form_fields
            form_fields.update(dict(source_nodes=self.sources))
            return form_fields

        def setUp(self):
            super().setUp()

            self.second_source = DataNode(
                title='2nd Test Node Source',
                type=DataNodeType.READER,
                name='manual',
                params={
                    'raw_data': {
                        'columns': ['D', 'C', 'D'],
                        'data': [
                            ['2015-07-17', 200.0, ''],
                            ['2015-08-17', 600.0, '']
                        ]},
                    'is_time_series': True
                }
            )
            self.second_source.save()
            self.sources = [self.source, self.second_source]

            data_edge = DataEdge(
                source=self.second_source,
                dest=self.node)
            data_edge.save()

    class WriterTestCase(CalculatorTestCase):
        pass
