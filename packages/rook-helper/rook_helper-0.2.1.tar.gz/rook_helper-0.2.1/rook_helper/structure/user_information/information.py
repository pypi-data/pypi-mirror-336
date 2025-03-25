from rook_helper import convert_to_type
from rook_helper.structure import StructureBase


class Information(StructureBase):

    PILLAR = 'user_information'
    DATA_STRUCTURE_TYPE = 'user_info'
    DATA_TYPE = None

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

        data_json.update({
            'metadata': cls.build_metadata(**_data)
            })

        data_json['metadata'].pop('was_the_user_under_physical_activity_bool')

        data_json['user_information']['user_body_metrics'] = cls._user_body_data(_data)
        data_json['user_information']['user_demographics'] = cls._user_demographics_data(_data)

        return data_json

    @staticmethod
    def _user_body_data(_data: dict) -> dict:

        return {
            'weight_kg_float': convert_to_type(_data.get('weight_kg_number', None), float),
            'height_cm_int': convert_to_type(_data.get('height_cm_number', None), int),
            'bmi_float': convert_to_type(_data.get('bmi_number', None), float)
            }

    @staticmethod
    def _user_demographics_data(_data: dict) -> dict:

        return {
            'sex_string': convert_to_type(_data.get('sex', None), str),
            'gender_string': convert_to_type(_data.get('gender', None), str),
            'date_of_birth_string': convert_to_type(_data.get('date_of_birth', None), str),
            'country_string': convert_to_type(_data.get('country', None), str),
            'state_string': convert_to_type(_data.get('state', None), str),
            'city_string': convert_to_type(_data.get('city', None), str),
            'ethnicity_string': convert_to_type(_data.get('ethnicity', None), str),
            'income_string': convert_to_type(_data.get('income', None), str),
            'marital_status_string': convert_to_type(_data.get('marital_status', None), str),
            'time_zone_string': convert_to_type(_data.get('time_zone', None), str),
            'education_string': convert_to_type(_data.get('education', None), str),
            }


build_json = Information.build_json

__all__ = ['build_json']
