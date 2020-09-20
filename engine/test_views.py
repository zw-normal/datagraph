from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from graph.models import DataNode, DataNodeType, DataEdge

class ViewsTestCase(TestCase):
    client = Client()

    @classmethod
    def setUpClass(cls):
        super(ViewsTestCase, cls).setUpClass()

        user = User.objects.create(
            username='engine-views')
        user.set_password('12345')
        user.save()

    def setUp(self) -> None:
        self.source_node = DataNode(
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
        self.source_node.save()

        self.target_node = DataNode(
            title='Test Node Target',
            type=DataNodeType.WRITER,
            name='vega_line',
            params={
                'column_titles': [
                    {'column': 'A', 'title': 'Title A'},
                    {'column': 'B', 'title': 'Title B'},
                ]
            }
        )
        self.target_node.save()

        data_edge = DataEdge(
            source=self.source_node,
            dest=self.target_node)
        data_edge.save()

    def test_workbench(self):
        self.client.login(
            username='engine-views', password='12345')

        response = self.client.get('/engine/')
        self.assertEqual(response.status_code, 200)

    def test_new_node_editor(self):
        self.client.login(
            username='engine-views', password='12345')

        response = self.client.get(
            '/engine/node-editor/reader/rba/')
        self.assertEqual(response.status_code, 200)

    def test_existing_node_editor(self):
        self.client.login(
            username='engine-views', password='12345')

        response = self.client.get(
            '/engine/node-editor/{}/'.format(self.source_node.id))
        self.assertEqual(response.status_code, 200)

    def test_delete_node(self):
        self.client.login(
            username='engine-views', password='12345')

        response = self.client.get(
            '/engine/node-editor/{}/delete'.format(self.target_node.id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/engine/')

    def test_cannot_delete_node(self):
        self.client.login(
            username='engine-views', password='12345')

        response = self.client.get(
            '/engine/node-editor/{}/delete'.format(self.source_node.id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '/engine/node-editor/{}/'.format(self.source_node.id))

    def test_vega_spec(self):
        response = self.client.get(
            '/engine/vega-spec/{}/'.format(self.target_node.id))
        self.assertEqual(response.status_code, 200)
