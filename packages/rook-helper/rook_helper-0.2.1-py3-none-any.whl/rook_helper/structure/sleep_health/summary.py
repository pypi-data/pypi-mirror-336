from rook_helper import format_datetime, convert_to_type
from rook_helper.structure import StructureBase, GranularData


class Summary(StructureBase):

    PILLAR = 'sleep_health'
    DATA_STRUCTURE_TYPE = 'sleep_summary'
    DATA_TYPE = 'summary'

    @classmethod
    def build_json(cls, _data: dict) -> dict:

        if not _data:
            raise ValueError('The data is empty')

        _data.update({
            'pillar': cls.PILLAR,
            'data_structure_type': cls.DATA_STRUCTURE_TYPE,
            'data_type': cls.DATA_TYPE
            })

        data_json = cls.build_data_structure(**_data)

        events = []

        events.append({
            'metadata': cls.build_metadata(**_data),
            'sleep_summary': cls.summary_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def summary_data(cls, _data: dict) -> dict:

        return {
            'breathing': cls._breathing_data(_data),
            'duration': cls._duration_data(_data),
            'heart_rate': cls._heart_rate_data(_data),
            'scores': cls._scores_rate_data(_data),
            'temperature': cls.temperature_data(_data)
            }

    @staticmethod
    def _breathing_data(_data: dict) -> dict:

        return {
            'breaths_minimum_per_min_int': convert_to_type(
                _data.get('breaths_minimum_per_min', None), int),
            'breaths_avg_per_min_int': convert_to_type(
                _data.get('breaths_avg_per_min', None), int),
            'breaths_maximum_per_min_int': convert_to_type(
                _data.get('breaths_max_per_min', None), int),
            'snoring_events_count_int': convert_to_type(
                _data.get('snoring_events_count_number', None), int),
            'snoring_duration_total_seconds_int': convert_to_type(
                _data.get('snoring_duration_total_seconds', None), int),
            'saturation_avg_percentage_int': convert_to_type(
                _data.get('saturation_avg_percentage', None), int),
            'saturation_minimum_percentage_int': convert_to_type(
                _data.get('saturation_min_percentage', None), int),
            'saturation_maximum_percentage_int': convert_to_type(
                _data.get('saturation_max_percentage', None), int),
            'breathing_granular_data_array': GranularData.breathing_granular_data(
                _data, 'breathing_granular_data_breaths_per_min'),
            'snoring_granular_data_array': GranularData.snoring_granular_data(
                _data, 'snoring_granular_data_snores'),
            'saturation_granular_data_array': GranularData.saturation_granular_data(
                _data, 'saturation_granular_data_percentage'),
            }

    @staticmethod
    def _duration_data(_data: dict) -> dict:

        return {
            'sleep_start_datetime_string': format_datetime(
                _data.get('sleep_start_datetime', None)),
            'sleep_end_datetime_string': format_datetime(_data.get('sleep_end_datetime', None)),
            'sleep_date_string': format_datetime(_data.get('sleep_date', None)),
            'sleep_duration_seconds_int': convert_to_type(
                _data.get('sleep_duration_seconds', None), int),
            'time_in_bed_seconds_int': convert_to_type(
                _data.get('time_in_bed_seconds', None), int),
            'light_sleep_duration_seconds_int': convert_to_type(
                _data.get('light_sleep_duration_seconds', None), int),
            'rem_sleep_duration_seconds_int': convert_to_type(
                _data.get('rem_sleep_duration_seconds', None), int),
            'deep_sleep_duration_seconds_int': convert_to_type(
                _data.get('deep_sleep_duration_seconds', None), int),
            'time_to_fall_asleep_seconds_int': convert_to_type(
                _data.get('time_to_fall_asleep_seconds', None), int),
            'time_awake_during_sleep_seconds_int': convert_to_type(
                _data.get('time_awake_during_sleep_seconds', None), int)
            }

    @staticmethod
    def _heart_rate_data(_data: dict) -> dict:

        return {
            'hr_maximum_bpm_int': convert_to_type(_data.get('hr_max_bpm', None), int),
            'hr_minimum_bpm_int': convert_to_type(_data.get('hr_minimum_bpm', None), int),
            'hr_avg_bpm_int': convert_to_type(_data.get('hr_avg_bpm', None), int),
            'hr_resting_bpm_int': convert_to_type(_data.get('hr_resting_bpm', None), int),
            'hrv_avg_rmssd_float': convert_to_type(_data.get('hrv_avg_rmssd_number', None), float),
            'hrv_avg_sdnn_float': convert_to_type(_data.get('hrv_avg_sdnn_number', None), float),
            'hr_granular_data_array': GranularData.heart_rate_granular_data(
                _data, 'hr_granular_data_bpm', 'hr_bpm', 'hr_bpm_int', False),
            'hrv_sdnn_granular_data_array': GranularData.heart_rate_granular_data(
                _data, 'hrv_sdnn_granular_data_number', 'hrv_sdnn', 'hrv_sdnn_float', True),
            'hrv_rmssd_granular_data_array': GranularData.heart_rate_granular_data(
                _data, 'hrv_rmssd_granular_data_number', 'hrv_rmssd', 'hrv_rmssd_float', True)
            }

    @staticmethod
    def _scores_rate_data(_data: dict) -> dict:

        return {
            'sleep_quality_rating_1_5_score_int': convert_to_type(
                _data.get('sleep_quality_rating_1_5_score', None), int),
            'sleep_efficiency_1_100_score_int': convert_to_type(
                _data.get('sleep_efficiency_1_100_score', None), int),
            'sleep_goal_seconds_int': convert_to_type(_data.get('sleep_goal_seconds', None), int),
            'sleep_continuity_1_5_score_int': convert_to_type(
                _data.get('sleep_continuity_1_5_score', None), int),
            'sleep_continuity_1_5_rating_int': convert_to_type(
                _data.get('sleep_continuity_1_5_rating', None), int)
            }

    @classmethod
    def temperature_data(cls, _data: dict) -> dict:

        temperature_avg_celsius = GranularData.temperature_granular_data(
            _data, 'temperature_avg_celsius', True)

        if temperature_avg_celsius:
            temperature_avg_celsius_object = temperature_avg_celsius
        else:
            temperature_avg_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_max_celsius = GranularData.temperature_granular_data(
            _data, 'temperature_max_celsius', True)

        if temperature_max_celsius:
            temperature_max_object = temperature_max_celsius
        else:
            temperature_max_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_min_celsius = GranularData.temperature_granular_data(
            _data, 'temperature_minimum_celsius', True)

        if temperature_min_celsius:
            temperature_min_celsius_object = temperature_min_celsius
        else:
            temperature_min_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_delta_celsius = GranularData.temperature_granular_data(
            _data, 'temperature_delta_celsius', True)

        if temperature_delta_celsius:
            temperature_delta_celsius_object = temperature_delta_celsius
        else:
            temperature_delta_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        return {
            'temperature_avg_object': temperature_avg_celsius_object,
            'temperature_maximum_object': temperature_max_object,
            'temperature_minimum_object': temperature_min_celsius_object,
            'temperature_delta_object': temperature_delta_celsius_object,
            'temperature_granular_data_array': GranularData.temperature_granular_data(
                _data, 'temperature_granular_data_celsius')
            }


build_json = Summary.build_json

__all__ = ['build_json']
