from tests import BaseTestClass

from rook_helper.structure.granular_data import GranularData
from tests.helper_test import check_result_schema

from tests.factory_granular_data_json import (
    blood_glucose_event_json, activity_event_json, blood_pressure_event_json,
    sleep_summary_granular_data_json, physical_summary_granular_data_json, body_summary_json,
    temperature_event_json, stress_event_json, oxygenation_event_json)

from tests.factory_granular_data_schema import (
    blood_glucose_granular_data_schema, activity_level_granular_data_schema,
    blood_pressure_granular_data_schema, breathing_granular_data_schema,
    elevation_granular_data_schema, floors_climbed_granular_data_schema,
    hrv_sdnn_granular_data_schema, hrv_rmssd_granular_data_schema, hr_granular_data_schema,
    hydration_amount_granular_data_schema, hydration_level_granular_data_schema,
    mood_granular_data_schema, temperature_granular_data_schema, temperature_avg_schema,
    temperature_delta_schema, temperature_maximum_schema, temperature_minimum_schema,
    saturation_granular_data_schema, snoring_granular_data_schema, steps_granular_data_schema,
    stress_granular_data_schema, swimming_distance_granular_data_schema,
    traveled_distance_granular_data_schema, tss_granular_data_schema, vo2_granular_data_schema)


class TestExample(BaseTestClass):

    @classmethod
    def setUpClass(cls):
        cls.seeds = [
            ('blood_glucose_granular_data_mg_per_dL_number', blood_glucose_event_json(),
             'blood_glucose_granular_data_array', blood_glucose_granular_data_schema(),
             'blood_glucose_granular_data', None),
            ('activity_level_granular_data_number', activity_event_json(),
             'activity_level_granular_data_array', activity_level_granular_data_schema(),
             'activity_granular_data', None),
            ('blood_pressure_granular_data_systolic_diastolic_bp_number',
             blood_pressure_event_json(), 'blood_pressure_granular_data_array',
             blood_pressure_granular_data_schema(), 'blood_pressure_granular_data', None),
            ('breathing_granular_data_breaths_per_min', sleep_summary_granular_data_json(),
             'breathing_granular_data_array', breathing_granular_data_schema(),
             'breathing_granular_data', None),
            ('elevation_granular_data_meters', activity_event_json(),
             'elevation_granular_data_array', elevation_granular_data_schema(),
             'elevation_granular_data', None),
            ('floors_climbed_granular_data_floors_number', physical_summary_granular_data_json(),
             'floors_climbed_granular_data_array', floors_climbed_granular_data_schema(),
             'floors_climbed_granular_data', None),
            ('hrv_sdnn_granular_data', body_summary_json(),
             'hrv_sdnn_granular_data_array', hrv_sdnn_granular_data_schema(),
             'heart_rate_granular_data', ['hrv_sdnn', 'hrv_sdnn_float', True]),
            ('hrv_rmssd_granular_data', body_summary_json(),
             'hrv_rmssd_granular_data_array', hrv_rmssd_granular_data_schema(),
             'heart_rate_granular_data', ['hrv_rmssd', 'hrv_rmssd_float', True]),
            ('hr_granular_data_bpm', body_summary_json(),
             'hr_granular_data_array', hr_granular_data_schema(),
             'heart_rate_granular_data', ['hr_bpm', 'hr_bpm_int', False]),
            ('hydration_amount_granular_data_ml_number', body_summary_json(),
             'hydration_amount_granular_data_array', hydration_amount_granular_data_schema(),
             'hydration_granular_data', ['hydration_amount_ml', 'hydration_amount_mL_int']),
            ('hydration_level_granular_data_percentage_number', body_summary_json(),
             'hydration_level_granular_data_percentage_number',
             hydration_level_granular_data_schema(), 'hydration_granular_data',
             ['hydration_level_percentage', 'hydration_level_percentage_int']),
            ('mood_granular_data_scale', body_summary_json(),
             'mood_granular_data_array', mood_granular_data_schema(), 'mood_granular_data', None),
            ('temperature_granular_data_celsius', sleep_summary_granular_data_json(),
             'temperature_granular_data_array', temperature_granular_data_schema(),
             'temperature_granular_data', [False]),
            ('temperature_avg_celsius', temperature_event_json(), 'temperature_avg_object',
             temperature_avg_schema(), 'temperature_granular_data', [True]),
            ('temperature_max_celsius', temperature_event_json(), 'temperature_maximum_object',
             temperature_maximum_schema(), 'temperature_granular_data', [True]),
            ('temperature_minimum_celsius', temperature_event_json(), 'temperature_minimum_object',
             temperature_minimum_schema(), 'temperature_granular_data', [True]),
            ('temperature_delta_celsius', temperature_event_json(), 'temperature_delta_object',
             temperature_delta_schema(), 'temperature_granular_data', [True]),
            ('saturation_granular_data_percentage', sleep_summary_granular_data_json(),
             'saturation_granular_data_array', saturation_granular_data_schema(),
             'saturation_granular_data', None),
            ('snoring_granular_data_snores', sleep_summary_granular_data_json(),
             'snoring_granular_data_array', snoring_granular_data_schema(),
             'snoring_granular_data', None),
            ('steps_granular_data_steps_per_min', activity_event_json(),
             'steps_granular_data_array', steps_granular_data_schema(),
             'steps_granular_data', None),
            ('stress_granular_data_score_number', physical_summary_granular_data_json(),
             'stress_granular_data_array', stress_granular_data_schema(),
             'stress_granular_data', None),
            ('swimming_distance_granular_data_meters', physical_summary_granular_data_json(),
             'swimming_distance_granular_data_array', swimming_distance_granular_data_schema(),
             'swimming_granular_data', None),
            ('traveled_distance_granular_data_meters', activity_event_json(),
             'traveled_distance_granular_data_array', traveled_distance_granular_data_schema(),
             'traveled_granular_data', None),
            ('tss_granular_data_1_500_score_number', stress_event_json(),
             'tss_granular_data_array', tss_granular_data_schema(),
             'tss_granular_data', None),
            ('vo2_granular_data_ml_per_min', oxygenation_event_json(), 'vo2_granular_data_array',
             vo2_granular_data_schema(), 'vo2_granular_data', None)
            ]

    def test_granular_data_success(self):

        for (_variable_name,
             _data,
             _variable_name_expect,
             _seed_json_expect,
             _function_name,
             _complement) in self.seeds:

            function_to_call = getattr(GranularData, _function_name)

            if not _complement:
                call_function = function_to_call(_data, _variable_name)
            else:
                if _function_name == 'heart_rate_granular_data':
                    call_function = function_to_call(_data,
                                                     _variable_name,
                                                     _complement[0],
                                                     _complement[1],
                                                     _complement[2])
                elif _function_name == 'temperature_granular_data':
                    call_function = function_to_call(_data,
                                                     _variable_name,
                                                     _complement[0])
                else:
                    call_function = function_to_call(_data,
                                                     _variable_name,
                                                     _complement[0],
                                                     _complement[1])

            result = {_variable_name_expect: call_function}

            self.assertTrue(check_result_schema(result, _seed_json_expect))

            input_list = result[_variable_name_expect]
            expected_list = _seed_json_expect[_variable_name_expect]

            self.assertEqual(len(input_list), len(expected_list))

            if _variable_name_expect not in ['temperature_avg_object', 'temperature_delta_object',
                                             'temperature_maximum_object',
                                             'temperature_minimum_object']:

                for input_item, expected_item in zip(input_list, expected_list):
                    self.assertSetEqual(set(input_item.keys()), set(expected_item.keys()))
