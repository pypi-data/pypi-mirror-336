from tests import BaseTestClass

from rook_helper.structure.body_health import Summary as BodySummary
from rook_helper.structure.sleep_health import Summary as SleepSummary
from rook_helper.structure.physical_health import Summary as physicalSummary
from tests.factory_json import body_health_summary_json, sleep_summary_json, physical_summary_json


class TestSummaryJsonStructure(BaseTestClass):

    @classmethod
    def setUpClass(cls):

        cls.seeds = [
            (body_health_summary_json(), BodySummary, 'body_health', 'body_summary', 'summary',
             ['blood_glucose', 'blood_pressure', 'body_metrics', 'heart_rate', 'hydration',
              'menstruation', 'mood', 'nutrition', 'oxygenation', 'temperature']),
            (sleep_summary_json(), SleepSummary, 'sleep_health', 'sleep_summary', 'summary',
             ['duration', 'scores', 'heart_rate', 'temperature', 'breathing']),
            (physical_summary_json(), physicalSummary, 'physical_health', 'physical_summary',
             'summary', ['activity', 'calories', 'distance', 'heart_rate', 'oxygenation',
                         'stress'])
            ]

    def test_summary_json_structure_success(self):

        for (expectative_json,
             structure_object,
             pillar,
             data_structure,
             data_type,
             content) in self.seeds:

            result = structure_object.build_json(expectative_json)
            event_type = result[pillar][data_type][data_structure]

            self.assertEqual(event_type[0]['metadata']['user_id_string'], self.user_id[:-9])
            self.assertIn('metadata', event_type[0])
            self.assertIn(data_structure, event_type[0])

            for item in content:
                self.assertIn(item, event_type[0][data_structure])

            self.assertIn('non_structured_data_array', event_type[0])

    def test_summary_json_structure_without_params(self):
        expectative = ['', None]

        for (_, structure_object, _, _, _, _) in self.seeds:

            for expect_item in expectative:
                with self.assertRaises(ValueError):
                    structure_object.build_json(expect_item)
