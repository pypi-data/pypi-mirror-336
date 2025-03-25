from tests import BaseTestClass

from rook_helper.structure.structure_base import StructureBase
from tests.factory_schemas import expectative_metadata
from tests.helper_test import check_result_schema


class TestSBMetadata(BaseTestClass):

    def test_sb_metadata_success(self):
        expectative_json = expectative_metadata()

        result = StructureBase.build_metadata(client_uuid=self.client_uuid,
                                              user_id=self.user_id,
                                              datetime='2023-08-09 15:30:50',
                                              sources_of_data='Polar',
                                              was_the_user_under_physical_activity=False)

        self.assertEqual(result['user_id_string'], self.user_id[:-9])
        self.assertEqual(result['datetime_string'], '2023-08-09T15:30:50.000000Z')
        self.assertTrue(check_result_schema(result, expectative_json))

    def test_metadata_success_data(self):
        expectative_json = expectative_metadata()

        data = {
            'client_uuid': self.client_uuid,
            'user_id': self.user_id,
            'datetime': '2023-08-09 15:30:50',
            'sources_of_data': 'Polar',
            'was_the_user_under_physical_activity': False,
            'test': 1,
            'test_2': True,
            'Test_3': 'hi'
            }

        result = StructureBase.build_metadata(**data)

        self.assertEqual(result['user_id_string'], self.user_id[:-9])
        self.assertEqual(result['datetime_string'], '2023-08-09T15:30:50.000000Z')
        self.assertTrue(check_result_schema(result, expectative_json))

    def test_sb_metadata_without_sources_of_data(self):
        with self.assertRaises(ValueError):
            StructureBase.build_metadata(client_uuid=self.client_uuid,
                                         user_id=self.user_id,
                                         datetime='2023-08-09 15:30:50',
                                         was_the_user_under_physical_activity=False)

    def test_sb_metadata_without_sources_of_data_empty(self):
        with self.assertRaises(ValueError):
            StructureBase.build_metadata(client_uuid=self.client_uuid,
                                         user_id=self.user_id,
                                         datetime='2023-08-09 15:30:50',
                                         sources_of_data='',
                                         was_the_user_under_physical_activity=False)

    def test_sb_metadata_without_params(self):
        with self.assertRaises(ValueError):
            StructureBase.build_metadata()

    def test_sb_metadata_incorrect_value(self):
        with self.assertRaises(ValueError):
            StructureBase.build_metadata(client_uuid=123,
                                         user_id=True,
                                         datetime='20',
                                         sources_of_data='df',
                                         was_the_user_under_physical_activity='False')
