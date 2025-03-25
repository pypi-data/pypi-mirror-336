from rook_helper import convert_to_type
from rook_helper.structure import StructureBase, GranularData


class StressEvent(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'stress_event'
    DATA_TYPE = 'events'

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
            'stress': cls.stress_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def stress_data(cls, _data: dict) -> dict:

        return {
            'stress_at_rest_duration_seconds_int': convert_to_type(
                _data.get('stress_at_rest_duration_seconds', None), int),
            'stress_duration_seconds_int': convert_to_type(
                _data.get('stress_duration_seconds', None), int),
            'low_stress_duration_seconds_int': convert_to_type(
                _data.get('low_stress_duration_seconds', None), int),
            'medium_stress_duration_seconds_int': convert_to_type(
                _data.get('medium_stress_duration_seconds', None), int),
            'high_stress_duration_seconds_int': convert_to_type(
                _data.get('high_stress_duration_seconds', None), int),
            'stress_avg_level_int': convert_to_type(
                _data.get('stress_avg_level_number', None), int),
            'stress_maximum_level_int': convert_to_type(
                _data.get('stress_max_level_number', None), int),
            'tss_granular_data_array': GranularData.stress_granular_data(
                _data, 'tss_granular_data_1_500_score_number')
            }


build_json = StressEvent.build_json

__all__ = ['build_json']
