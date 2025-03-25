from rook_helper import convert_to_type
from rook_helper.structure import StructureBase


class BodyMetricsEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'body_metrics_event'
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
            'body_metrics': cls.body_metrics_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def body_metrics_data(cls, _data: dict) -> dict:

        return {
            'waist_circumference_cm_int': convert_to_type(
                _data.get('waist_circumference_cm_number', None), int),
            'hip_circumference_cm_int': convert_to_type(
                _data.get('hip_circumference_cm_number', None), int),
            'chest_circumference_cm_int': convert_to_type(
                _data.get('chest_circumference_cm_number', None), int),
            'bone_composition_percentage_int': convert_to_type(
                _data.get('bone_composition_percentage_number', None), int),
            'muscle_composition_percentage_int': convert_to_type(
                _data.get('muscle_composition_percentage_number', None), int),
            'water_composition_percentage_int': convert_to_type(
                _data.get('water_composition_percentage_number', None), int),
            'weight_kg_float': convert_to_type(_data.get('weight_kg_number', None), float),
            'height_cm_int': convert_to_type(_data.get('height_cm_number', None), int),
            'bmi_float': convert_to_type(_data.get('bmi_number', None), float)
            }


build_json = BodyMetricsEvent.build_json

__all__ = ['build_json']
