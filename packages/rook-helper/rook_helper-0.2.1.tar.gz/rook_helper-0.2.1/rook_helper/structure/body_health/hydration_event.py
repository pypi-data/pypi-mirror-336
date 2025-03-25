from rook_helper import convert_to_type
from rook_helper.structure import StructureBase, GranularData


class HydrationEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'hydration_event'
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
            'hydration': cls.hydration_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def hydration_data(cls, _data: dict) -> dict:

        return {
            'water_total_consumption_mL_int': convert_to_type(
                _data.get('water_total_consumption_ml_number', None), int),
            'hydration_amount_granular_data_array': GranularData.hydration_granular_data(
                _data, 'hydration_amount_granular_data_ml_number', 'hydration_amount_ml',
                'hydration_amount_mL_int'),
            'hydration_level_granular_data_array': GranularData.hydration_granular_data(
                _data, 'hydration_level_granular_data_percentage_number',
                'hydration_level_percentage', 'hydration_level_percentage_int')
            }


build_json = HydrationEvent.build_json

__all__ = ['build_json']
