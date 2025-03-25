from tests import BaseTestClass
from rook_helper.convert import convert_to_type


class TestFormatDatetime(BaseTestClass):

    def test_variable_convert_int_success(self):

        seed = ['3', 3, 3.1]

        for item in seed:
            result = convert_to_type(item, int)
            self.assertEqual(result, 3)

    def test_variable_convert_float_success(self):

        seed = ['3.0', 3, 3.0]

        for item in seed:
            result = convert_to_type(item, float)
            self.assertEqual(result, 3)

    def test_variable_convert_str_success(self):

        result_1 = convert_to_type('hola', str)
        self.assertEqual(result_1, 'hola')

        result_2 = convert_to_type('3.1', str)
        self.assertEqual(result_2, '3.1')

        result_3 = convert_to_type('3', str)
        self.assertEqual(result_3, '3')

    def test_variable_convert_none(self):
        result_int = convert_to_type(None, int)
        self.assertEqual(result_int, None)

        result_float = convert_to_type(None, float)
        self.assertEqual(result_float, None)

        result_str = convert_to_type(None, str)
        self.assertEqual(result_str, None)

    def test_variable_convert_str_empty(self):
        result_str = convert_to_type('', str)

        self.assertEqual(result_str, None)

    def test_variable_convert_not_int_or_float(self):
        seed = [int, float]

        for item in seed:
            result = convert_to_type('hola', item)
            self.assertEqual(result, None)

    def test_variable_convert_not_bool(self):
        seed = [123, 'hola', 'float']

        for item in seed:
            result = convert_to_type(item, bool)
            self.assertEqual(result, None)

    def test_variable_convert_is_bool(self):
        seed = [True, False]

        for item in seed:
            result = convert_to_type(item, bool)
            self.assertEqual(result, item)
