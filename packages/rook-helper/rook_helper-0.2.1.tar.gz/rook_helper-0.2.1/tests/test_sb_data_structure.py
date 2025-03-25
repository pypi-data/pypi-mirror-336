from tests import BaseTestClass

from rook_helper.structure.structure_base import StructureBase
from tests.factory_schemas import expectative_data_structure
from tests.helper_test import check_result_schema


class TestSBDataStructure(BaseTestClass):

    def test_sb_data_structure_success(self):

        seeds = [
            ('body_health', 'blood_glucose_event', 'events', False)
            ]

        for pillar_item, struct_item, data_type_item, detected_item in seeds:
            expectative_json = expectative_data_structure(pillar_item, data_type_item)

            result = StructureBase.build_data_structure(pillar=pillar_item,
                                                        data_structure_type=struct_item,
                                                        data_type=data_type_item,
                                                        client_uuid=self.client_uuid,
                                                        user_id=self.user_id,
                                                        document_version=1,
                                                        auto_detected=detected_item)

            self.assertTrue(check_result_schema(result, expectative_json))
            self.assertIn(pillar_item, result)
            self.assertEqual(result['data_structure'], struct_item)
            self.assertEqual(result['client_uuid'], self.client_uuid)
            self.assertEqual(result['user_id'], self.user_id)

    def test_sb_data_structure_with_pillar_empty(self):
        with self.assertRaises(ValueError):
            StructureBase.build_data_structure(pillar='',
                                               data_structure_type='blood_glucose_event',
                                               data_type='events',
                                               client_uuid=self.client_uuid,
                                               user_id=self.user_id,
                                               document_version=1,
                                               auto_detected=True)

    def test_sb_data_structure_with_pillar_no_exists(self):
        with self.assertRaises(ValueError):
            StructureBase.build_data_structure(pillar='body',
                                               data_structure_type='blood_glucose_event',
                                               data_type='events',
                                               client_uuid=self.client_uuid,
                                               user_id=self.user_id,
                                               document_version=1,
                                               auto_detected=True)

    def test_sb_data_structure_with_without_pillar(self):
        with self.assertRaises(ValueError):
            StructureBase.build_data_structure(data_structure_type='blood_glucose_event',
                                               data_type='events',
                                               client_uuid=self.client_uuid,
                                               user_id=self.user_id,
                                               document_version=1,
                                               auto_detected=True)

    def test_sb_data_structure_without_params(self):
        with self.assertRaises(ValueError):
            StructureBase.build_data_structure()

    def test_sb_data_structure_incorrect_value(self):
        with self.assertRaises(ValueError):
            StructureBase.build_data_structure(pillar=123,
                                               data_structure_type='blood_glucose_event',
                                               data_type='events',
                                               client_uuid=self.client_uuid,
                                               user_id=self.user_id,
                                               document_version=1,
                                               auto_detected='hi')

    def test_sb_data_structure_with_document_version_0(self):
        with self.assertRaises(ValueError):
            StructureBase.build_data_structure(pillar='body_health',
                                               data_structure_type='blood_glucose_event',
                                               data_type='events',
                                               client_uuid=self.client_uuid,
                                               user_id=self.user_id,
                                               document_version=0,
                                               auto_detected=True)
