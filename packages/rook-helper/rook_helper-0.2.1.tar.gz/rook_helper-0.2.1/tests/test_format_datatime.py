from tests import BaseTestClass
from rook_helper.format import format_datetime


class TestFormatDatetime(BaseTestClass):

    def test_format_datetime_success(self):
        expectative = [
            ('2023-08-09', '2023-08-09T00:00:00.000000Z'),
            ('2023-08-09 15:30:50', '2023-08-09T15:30:50.000000Z'),
            ('2023-08-09T15:30:50', '2023-08-09T15:30:50.000000Z'),
            ('2023-08-09T15:30:50.4567', '2023-08-09T15:30:50.456700Z'),
            ('2023-08-09T15:30:50.4567Z', '2023-08-09T15:30:50.456700Z'),
            ('2023-08-09T15:30:50.456795438Z', '2023-08-09T15:30:50.456795Z'),
            ('2023-08-09T15:30:50.4567-05', '2023-08-09T15:30:50.456700-05:00'),
            ('2023-08-09T15:30:50.4567-0600', '2023-08-09T15:30:50.456700-06:00'),
            ('2023-08-09T15:30:50.4567+0230', '2023-08-09T15:30:50.456700+02:30'),
            ('2023-08-09T15:30:50.4567+02:00', '2023-08-09T15:30:50.456700+02:00')
            ]

        for test_item, expectative_item in expectative:
            result = format_datetime(test_item)

            self.assertEqual(result, expectative_item)

    def test_format_datetime_invalid_datetime(self):
        expectative = ['july 8', 'kdd', '2023/08/09', '']

        for item_test in expectative:
            with self.assertRaises(ValueError):
                format_datetime(item_test)

    def test_format_datetime_is_number_or_bool(self):
        expectative = [123, True, False]

        for item_test in expectative:
            with self.assertRaises(TypeError):
                format_datetime(item_test)

    def test_format_datetime_is_none(self):
        result = format_datetime(None)
        self.assertEqual(result, None)
