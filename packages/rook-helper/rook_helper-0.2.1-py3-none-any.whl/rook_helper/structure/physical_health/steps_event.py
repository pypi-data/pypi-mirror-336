from rook_helper import convert_to_type
from rook_helper.structure import StructureBase


class StepsEvent(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'steps_event'
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
            'steps': cls.steps_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def steps_data(cls, _data: dict) -> dict:

        return {
            'accumulated_steps_int': convert_to_type(_data.get('accumulated_steps_int', 0), int)
            }


build_json = StepsEvent.build_json

__all__ = ['build_json']
