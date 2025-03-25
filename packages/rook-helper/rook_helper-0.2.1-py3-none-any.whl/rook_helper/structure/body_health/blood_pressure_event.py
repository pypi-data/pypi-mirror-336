from rook_helper.structure import StructureBase, GranularData


class BloodPressureEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'blood_pressure_event'
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
            'blood_pressure': cls.blood_pressure_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def blood_pressure_data(cls, _data: dict) -> dict:

        blood_pressure_avg_array = GranularData.blood_pressure_granular_data(
            _data, 'blood_pressure_day_avg_systolic_diastolic_bp_number', True)

        if blood_pressure_avg_array:
            blood_pressure_avg_object = blood_pressure_avg_array
        else:
            blood_pressure_avg_object = {
                'systolic_mmHg_int': None,
                'diastolic_mmHg_int': None
                }

        return {
            'blood_pressure_avg_object': blood_pressure_avg_object,
            'blood_pressure_granular_data_array': GranularData.blood_pressure_granular_data(
                _data, 'blood_pressure_granular_data_systolic_diastolic_bp_number'),
            }


build_json = BloodPressureEvent.build_json

__all__ = ['build_json']
