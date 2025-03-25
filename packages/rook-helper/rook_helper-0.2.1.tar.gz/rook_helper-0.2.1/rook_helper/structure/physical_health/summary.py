from rook_helper import convert_to_type
from rook_helper.structure import StructureBase, GranularData
from rook_helper.structure.physical_health import (ActivityEvents, HeartRateEvent,
                                                   OxygenationEvent, StressEvent)


class Summary(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'physical_summary'
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
            'physical_summary': cls.summary_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def summary_data(cls, _data: dict) -> dict:

        return {
            'activity': cls.activity_data(_data),
            'calories': cls.calories_data(_data),
            'distance': cls.distance_data(_data),
            'heart_rate': HeartRateEvent.heart_rate_data(_data),
            'oxygenation': OxygenationEvent.oxygenation_data(_data),
            'stress': cls.stress_data(_data)
            }

    @classmethod
    def activity_data(cls, _data: dict) -> dict:

        activity = ActivityEvents.activity_data(_data)

        activity.pop('activity_start_datetime_string')
        activity.pop('activity_end_datetime_string')
        activity.pop('activity_duration_seconds_int')
        activity.pop('activity_type_name_string')
        activity.pop('activity_strain_level_float')
        activity.pop('activity_work_kilojoules_float')
        activity.pop('activity_energy_kilojoules_float')
        activity.pop('activity_energy_planned_kilojoules_float')

        return activity

    @classmethod
    def calories_data(cls, _data: dict) -> dict:

        calories = ActivityEvents.calories_data(_data)

        calories.pop('fat_percentage_of_calories_int')
        calories.pop('carbohydrate_percentage_of_calories_int')
        calories.pop('protein_percentage_of_calories_int')

        return calories

    @classmethod
    def distance_data(cls, _data: dict) -> dict:

        distance = ActivityEvents.distance_data(_data)

        distance.update(
            {
                'active_steps_int': convert_to_type(
                    _data.get('active_steps_per_day_number', None), int),
                'active_steps_granular_data_array': GranularData.active_steps_granular_data(
                    _data, 'active_steps_granular_data_steps_per_hr')
                }
            )

        return distance

    @classmethod
    def stress_data(cls, _data: dict) -> dict:

        stress = StressEvent.stress_data(_data)

        stress.pop('tss_granular_data_array')

        stress.update(
            {
                'stress_granular_data_array': GranularData.stress_granular_data(
                    _data, 'stress_granular_data_score_number')
                }
            )

        return stress
