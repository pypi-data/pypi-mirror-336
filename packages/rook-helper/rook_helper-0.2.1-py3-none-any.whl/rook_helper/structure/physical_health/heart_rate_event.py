from rook_helper import convert_to_type
from rook_helper.structure import StructureBase, GranularData


class HeartRateEvent(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'heart_rate_event'
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
            'heart_rate': cls.heart_rate_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def heart_rate_data(cls, _data: dict) -> dict:

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


build_json = HeartRateEvent.build_json

__all__ = ['build_json']
