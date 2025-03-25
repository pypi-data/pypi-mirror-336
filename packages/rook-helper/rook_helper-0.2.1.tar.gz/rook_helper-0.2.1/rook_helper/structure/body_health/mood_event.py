from rook_helper import convert_to_type
from rook_helper.structure import StructureBase, GranularData


class MoodEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'mood_event'
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
            'mood': cls.mood_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def mood_data(cls, _data: dict) -> dict:

        return {
            'mood_minimum_scale_int': convert_to_type(_data.get('mood_minimum_scale', None), int),
            'mood_avg_scale_int': convert_to_type(_data.get('mood_avg_scale', None), int),
            'mood_maximum_scale_int': convert_to_type(_data.get('mood_max_scale', None), int),
            'mood_delta_scale_int': convert_to_type(_data.get('mood_delta_scale', None), int),
            'mood_granular_data_array': GranularData.mood_granular_data(
                _data, 'mood_granular_data_scale')
            }


build_json = MoodEvent.build_json

__all__ = ['build_json']
