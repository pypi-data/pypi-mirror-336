from rook_helper.structure import StructureBase
from rook_helper.structure.body_health import (BodyMetricsEvent, BloodGlucoseEvent,
                                               BloodPressureEvent, HeartRateEvent, HydrationEvent,
                                               MoodEvent, MenstruationEvent, NutritionEvent,
                                               OxygenationEvent, TemperatureEvent)


class Summary(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'body_summary'
    DATA_TYPE = 'summary'

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
            'body_summary': cls.summary_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def summary_data(cls, _data: dict) -> dict:

        return {
            'blood_glucose': BloodGlucoseEvent.blood_glucose_data(_data),
            'blood_pressure': BloodPressureEvent.blood_pressure_data(_data),
            'body_metrics': BodyMetricsEvent.body_metrics_data(_data),
            'heart_rate': HeartRateEvent.heart_rate_data(_data),
            'hydration': HydrationEvent.hydration_data(_data),
            'menstruation': MenstruationEvent.menstruation_data(_data),
            'mood': MoodEvent.mood_data(_data),
            'nutrition': NutritionEvent.nutrition_data(_data),
            'oxygenation': OxygenationEvent.oxygenation_data(_data),
            'temperature': TemperatureEvent.temperature_data(_data)
            }


build_json = Summary.build_json

__all__ = ['build_json']
