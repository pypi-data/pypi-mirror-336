from tests import BaseTestClass

from rook_helper.structure.user_information import Information
from tests.factory_json import user_information_json


class TestUserInformation(BaseTestClass):

    def test_user_information_success(self):
        result = Information.build_json(user_information_json())

        self.assertIn('metadata', result)
        self.assertIn('user_information', result)

        event_type = result['user_information']

        self.assertIn('user_body_metrics', event_type)
        self.assertIn('user_demographics', event_type)

    def test_user_information_without_params(self):
        expectative = ['', None]

        for expect_item in expectative:
            with self.assertRaises(ValueError):
                Information.build_json(expect_item)
