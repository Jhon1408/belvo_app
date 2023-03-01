from django.test import TestCase

from .models import Enviroment
from .helpers.get_variable import get_variable


class EnviromentTestCase(TestCase):
    def setUp(self):
        Enviroment.objects.create(name="test", type="string", value="test")

    def test_enviroment(self):
        test = Enviroment.objects.get(name="test")
        self.assertEqual(test.name, "test")
        self.assertEqual(test.type, "string")
        self.assertEqual(test.value, "test")

    def test_get_variable_default_set(self):
        test = get_variable("invalid_variable", "test")
        self.assertEqual(test, "test")

    def test_get_variable_default_not_set(self):
        test = get_variable("test")
        self.assertEqual(test, "test")

    def test_get_variable_exception_handling(self):
        with self.assertRaises(Exception):
            get_variable("invalid_variable")
