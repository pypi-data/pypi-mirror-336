from tests import BaseTestClass
from tests.helper_test import check_result_schema
from rook_helper.structure.body_health import (BloodGlucoseEvent, BloodPressureEvent,
                                               BodyMetricsEvent, HeartRateEvent as HRBody,
                                               HydrationEvent, MenstruationEvent, MoodEvent,
                                               NutritionEvent, OxygenationEvent as OxBody,
                                               TemperatureEvent)

from rook_helper.structure.physical_health import (ActivityEvents, CaloriesEvent, HeartRateEvent,
                                                   OxygenationEvent, StepsEvent, StressEvent)


from tests.factory_json import (activity_events_json, blood_glucose_event_json,
                                blood_pressure_event_json, body_metrics_event_json,
                                heart_rate_event_body_json, hydration_event_json,
                                menstruation_event_json, mood_event_json, nutrition_event_json,
                                oxygenation_event_body_json, temperature_event_json,
                                calories_event_json, heart_rate_physical_event_json,
                                oxygenation_event_physical_json, steps_event_json,
                                stress_event_json)

from tests.factory_schemas import (activity_events, expectative_blood_glucose_event,
                                   expectative_blood_pressure_event,
                                   expectative_body_metrics_event, heart_rate_event_body_event,
                                   hydration_event, menstruation_event, mood_event,
                                   nutrition_event, oxygenation_event_body, temperature_event,
                                   calories_event, heart_rate_physical_event,
                                   oxygenation_physical_event, steps_event, stress_event)


class TestEventJsonStructure(BaseTestClass):

    @classmethod
    def setUpClass(cls):

        cls.seeds = [
            (expectative_blood_glucose_event(), blood_glucose_event_json(), BloodGlucoseEvent,
             'body_health', 'blood_glucose_event', 'events', 'blood_glucose'),
            (expectative_blood_pressure_event(), blood_pressure_event_json(), BloodPressureEvent,
             'body_health', 'blood_pressure_event', 'events', 'blood_pressure'),
            (expectative_body_metrics_event(), body_metrics_event_json(), BodyMetricsEvent,
             'body_health', 'body_metrics_event', 'events', 'body_metrics'),
            (heart_rate_event_body_event(), heart_rate_event_body_json(), HRBody,
             'body_health', 'heart_rate_event', 'events', 'heart_rate'),
            (hydration_event(), hydration_event_json(), HydrationEvent,
             'body_health', 'hydration_event', 'events', 'hydration'),
            (menstruation_event(), menstruation_event_json(), MenstruationEvent,
             'body_health', 'menstruation_event', 'events', 'menstruation'),
            (mood_event(), mood_event_json(), MoodEvent,
             'body_health', 'mood_event', 'events', 'mood'),
            (nutrition_event(), nutrition_event_json(), NutritionEvent,
             'body_health', 'nutrition_event', 'events', 'nutrition'),
            (oxygenation_event_body(), oxygenation_event_body_json(), OxBody,
             'body_health', 'oxygenation_event', 'events', 'oxygenation'),
            (temperature_event(), temperature_event_json(), TemperatureEvent,
             'body_health', 'temperature_event', 'events', 'temperature'),
            (calories_event(), calories_event_json(), CaloriesEvent,
             'physical_health', 'calories_event', 'events', 'calories'),
            (heart_rate_physical_event(), heart_rate_physical_event_json(), HeartRateEvent,
             'physical_health', 'heart_rate_event', 'events', 'heart_rate'),
            (oxygenation_physical_event(), oxygenation_event_physical_json(), OxygenationEvent,
             'physical_health', 'oxygenation_event', 'events', 'oxygenation'),
            (steps_event(), steps_event_json(), StepsEvent,
             'physical_health', 'steps_event', 'events', 'steps'),
            (stress_event(), stress_event_json(), StressEvent,
             'physical_health', 'stress_event', 'events', 'stress'),
            (activity_events(), activity_events_json(), ActivityEvents,
             'physical_health', 'activity_event', 'events', ['activity'])
            ]

    def test_event_json_structure_success(self):

        for (seed_structure_schema,
             expectative_json,
             structure_object,
             pillar,
             data_structure,
             data_type,
             key_item) in self.seeds:

            result = structure_object.build_json(expectative_json)

            event_type = result[pillar][data_type][data_structure]

            self.assertTrue(check_result_schema(result, seed_structure_schema))
            self.assertEqual(event_type[0]['metadata']['user_id_string'], self.user_id[:-9])
            self.assertIn('metadata', event_type[0])

            if not isinstance(key_item, list):
                self.assertIn(key_item, event_type[0])
            else:
                for item in key_item:
                    self.assertIn(item, event_type[0])

            self.assertIn('non_structured_data_array', event_type[0])

    def test_event_json_structure_without_params(self):
        expectative = ['', None]

        for (_, _, structure_object, _, _, _, _) in self.seeds:

            for expect_item in expectative:
                with self.assertRaises(ValueError):
                    structure_object.build_json(expect_item)
