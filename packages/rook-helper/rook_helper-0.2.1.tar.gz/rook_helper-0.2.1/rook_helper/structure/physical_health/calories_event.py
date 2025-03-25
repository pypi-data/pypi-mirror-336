from rook_helper import convert_to_type
from rook_helper.structure import StructureBase


class CaloriesEvent(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'calories_event'
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
            'calories': cls.calories_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def calories_data(cls, _data: dict) -> dict:

        return {
            'basal_float': convert_to_type(_data.get('basal_float', None), float),
            'active_float': convert_to_type(_data.get('active_float', None), float)
            }


build_json = CaloriesEvent.build_json

__all__ = ['build_json']
