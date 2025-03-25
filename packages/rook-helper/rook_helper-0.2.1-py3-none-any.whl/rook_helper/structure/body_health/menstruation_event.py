from rook_helper import convert_to_type
from rook_helper.structure import StructureBase, GranularData


class MenstruationEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'menstruation_event'
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
            'menstruation': cls.menstruation_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def menstruation_data(cls, _data: dict) -> dict:

        return {
            'last_updated_datetime_string': convert_to_type(
                _data.get('last_updated_datetime', None), str),
            'period_start_date_string': convert_to_type(_data.get('period_start_date', None), str),
            'cycle_day_int': convert_to_type(_data.get('cycle_day', None), int),
            'predicted_cycle_length_days_int': convert_to_type(
                _data.get('predicted_cycle_length_days', None), int),
            'cycle_length_days_int': convert_to_type(_data.get('cycle_length_days', None), int),
            'current_phase_string': convert_to_type(_data.get('current_phase', None), str),
            'length_of_current_phase_days_int': convert_to_type(
                _data.get('length_of_current_phase_days', None), int),
            'days_until_next_phase_int': convert_to_type(
                _data.get('days_until_next_phase', None), int),
            'is_a_predicted_cycle_bool': convert_to_type(
                _data.get('is_a_predicted_cycle', None), bool),
            'menstruation_flow_granular_data_array': GranularData.menstruation_granular_data(
                _data, 'menstruation_flow_ml_granular_data_number')
            }


build_json = MenstruationEvent.build_json

__all__ = ['build_json']
