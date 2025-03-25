from tests import BaseTestClass
from rook_helper.format import remove_client_uuid_from_user_id


class TestUserIdFormat(BaseTestClass):

    def test_user_id_formate_success(self):
        expectative = 'test'

        result = remove_client_uuid_from_user_id(self.user_id, self.client_uuid)

        self.assertEqual(result, expectative)

    def test_user_id_formate_no_uuid_in_client(self):
        expectative = ['abcdefgh-000-adc-xxxx-10d3f4f43127', 'abcdefgh', 123, None]

        message = 'Invalid client_uuid: must be a valid UUIDv4.'

        for item_test in expectative:
            with self.assertRaisesRegex(ValueError, message):
                remove_client_uuid_from_user_id(self.user_id, item_test)

    def test_user_id_formate_is_empty_or_none(self):
        expectative = ['', None]

        for item_test in expectative:
            with self.assertRaisesRegex(ValueError, 'The provided user_id is empty or None.'):
                remove_client_uuid_from_user_id(item_test,
                                                'abcdefgh-000-adc-xxxx-10d3f4f43127')

    def test_user_id_formate_client_uuid_different_user_id(self):
        message = 'Mismatch: The client_uuid prefix does not match the user_id.'

        with self.assertRaisesRegex(ValueError, message):
            remove_client_uuid_from_user_id('test-000000ec', self.client_uuid)
