from rook_helper import convert_to_type
from rook_helper.structure import StructureBase, GranularData


class OxygenationEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'oxygenation_event'
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
            'oxygenation': cls.oxygenation_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def oxygenation_data(cls, _data: dict) -> dict:

        return {
            'saturation_avg_percentage_int': convert_to_type(
                _data.get('saturation_avg_percentage', None), int),
            'vo2max_mL_per_min_per_kg_int': convert_to_type(
                _data.get('vo2max_ml_per_min_per_kg', None), int),
            'saturation_granular_data_array': GranularData.saturation_granular_data(
                _data, 'saturation_granular_data_percentage'),
            'vo2_granular_data_array': GranularData.vo2_granular_data(
                _data, 'vo2_granular_data_ml_per_min')
            }


build_json = OxygenationEvent.build_json

__all__ = ['build_json']
