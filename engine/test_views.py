from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


class ViewsTestCase(TestCase):
    client = Client()

    @classmethod
    def setUpClass(cls):
        super(ViewsTestCase, cls).setUpClass()

        user = User.objects.create(
            username='engine-views')
        user.set_password('12345')
        user.save()

    def test_workbench(self):
        self.client.login(
            username='engine-views', password='12345')

        response = self.client.get('/engine/')
        self.assertEqual(response.status_code, 200)

    def test_new_node_editor(self):
        self.client.login(
            username='engine-views', password='12345')

        response = self.client.get(
            '/engine/node_editor/reader/rba/')
        self.assertEqual(response.status_code, 200)
