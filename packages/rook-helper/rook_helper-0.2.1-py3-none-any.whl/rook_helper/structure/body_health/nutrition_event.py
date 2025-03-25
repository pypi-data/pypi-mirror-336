from rook_helper import convert_to_type
from rook_helper.structure import StructureBase


class NutritionEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'nutrition_event'
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
            'nutrition': cls.nutrition_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def nutrition_data(cls, _data: dict) -> dict:

        return {
            'food_intake_float': convert_to_type(_data.get('food_intake_number', None), float),
            'calories_intake_kcal_float': convert_to_type(
                _data.get('calories_intake_number', None), float),
            'protein_intake_g_float': convert_to_type(
                _data.get('protein_intake_g_number', None), float),
            'sugar_intake_g_float': convert_to_type(
                _data.get('sugar_intake_g_number', None), float),
            'fat_intake_g_float': convert_to_type(_data.get('fat_intake_g_number', None), float),
            'trans_fat_intake_g_float': convert_to_type(
                _data.get('trans_fat_intake_g_number', None), float),
            'carbohydrates_intake_g_float': convert_to_type(
                _data.get('carbohydrates_intake_g_number', None), float),
            'fiber_intake_g_float': convert_to_type(
                _data.get('fiber_intake_g_number', None), float),
            'alcohol_intake_g_float': convert_to_type(
                _data.get('alcohol_intake_g_number', None), float),
            'sodium_intake_mg_float': convert_to_type(
                _data.get('sodium_intake_mg_number', None), float),
            'cholesterol_intake_mg_float': convert_to_type(
                _data.get('cholesterol_intake_mg_number', None), float)
            }


build_json = NutritionEvent.build_json

__all__ = ['build_json']
