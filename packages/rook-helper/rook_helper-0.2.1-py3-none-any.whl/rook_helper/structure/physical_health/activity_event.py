from rook_helper import convert_to_type
from rook_helper.structure import StructureBase, GranularData
from rook_helper.structure.physical_health import (HeartRateEvent, OxygenationEvent, StressEvent)


class ActivityEvents(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'activity_event'
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
            'activity':  cls.activity_data(_data),
            'calories': cls.calories_data(_data),
            'distance': cls.distance_data(_data),
            'heart_rate': HeartRateEvent.heart_rate_data(_data),
            'movement': cls.movement_data(_data),
            'power': cls.power_data(_data),
            'position': cls.position_data(_data),
            'oxygenation': OxygenationEvent.oxygenation_data(_data),
            'stress': StressEvent.stress_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def activity_data(cls, _data: dict) -> dict:

        return {
            'activity_start_datetime_string': convert_to_type(
                _data.get('activity_start_time_date_time', None), str),
            'activity_end_datetime_string': convert_to_type(
                _data.get('activity_end_time_date_time', None), str),
            'activity_duration_seconds_int': convert_to_type(
                _data.get('activity_duration_seconds', None), int),
            'activity_type_name_string': convert_to_type(
                _data.get('activity_type_name', None), str),
            'active_seconds_int': convert_to_type(_data.get('active_seconds', None), int),
            'rest_seconds_int': convert_to_type(_data.get('rest_seconds', None), str),
            'low_intensity_seconds_int': convert_to_type(
                _data.get('low_intensity_seconds', None), int),
            'moderate_intensity_seconds_int': convert_to_type(
                _data.get('moderate_intensity_seconds', None), int),
            'vigorous_intensity_seconds_int': convert_to_type(
                _data.get('vigorous_intensity_seconds', None), int),
            'inactivity_seconds_int': convert_to_type(
                _data.get('inactivity_seconds', None), int),
            'continuous_inactive_periods_int': convert_to_type(
                _data.get('continuous_inactive_periods_number', None), int),
            'activity_strain_level_float': convert_to_type(
                _data.get('activity_strain_level_number', None), float),
            'activity_work_kilojoules_float': convert_to_type(
                _data.get('activity_work_kilojoules', None), float),
            'activity_energy_kilojoules_float': convert_to_type(
                _data.get('activity_energy_kilojoules', None), float),
            'activity_energy_planned_kilojoules_float': convert_to_type(
                _data.get('activity_energy_planned_kilojoules', None), float),
            'activity_level_granular_data_array': GranularData.activity_granular_data(
                _data, 'activity_level_granular_data_number'
                )
            }

    @classmethod
    def calories_data(cls, _data: dict) -> dict:

        return {
            'calories_net_intake_kcal_float': convert_to_type(
                _data.get('calories_net_intake_kilocalories', None), float),
            'calories_expenditure_kcal_float': convert_to_type(
                _data.get('calories_expenditure_kilocalories', None), float),
            'calories_net_active_kcal_float': convert_to_type(
                _data.get('calories_net_active_kilocalories', None), float),
            'calories_basal_metabolic_rate_kcal_float': convert_to_type(
                _data.get('calories_basal_metabolic_rate_kilocalories', None), float),
            'fat_percentage_of_calories_int': convert_to_type(
                _data.get('fat_percentage_of_calories_percentage', None), int),
            'carbohydrate_percentage_of_calories_int': convert_to_type(
                _data.get('carbohydrate_percentage_of_calories_percentage', None), int),
            'protein_percentage_of_calories_int': convert_to_type(
                _data.get('protein_percentage_of_calories_percentage', None), int)
            }

    @classmethod
    def distance_data(cls, _data: dict) -> dict:

        return {
            'steps_int': convert_to_type(_data.get('steps_number', None), int),
            'walked_distance_meters_float': convert_to_type(
                _data.get('walked_distance_meters', None), float),
            'traveled_distance_meters_float': convert_to_type(
                _data.get('traveled_distance_meters', None), float),
            'floors_climbed_float': convert_to_type(
                _data.get('floors_climbed_number', None), float),
            'elevation_avg_altitude_meters_float': convert_to_type(
                _data.get('elevation_avg_altitude_meters', None), float),
            'elevation_minimum_altitude_meters_float': convert_to_type(
                _data.get('elevation_minimum_altitude_meters', None), float),
            'elevation_maximum_altitude_meters_float': convert_to_type(
                _data.get('elevation_max_altitude_meters', None), float),
            'elevation_loss_actual_altitude_meters_float': convert_to_type(
                _data.get('elevation_loss_actual_altitude_meters', None), float),
            'elevation_gain_actual_altitude_meters_float': convert_to_type(
                _data.get('elevation_gain_actual_altitude_meters', None), float),
            'elevation_planned_gain_meters_float': convert_to_type(
                _data.get('elevation_planned_gain_meters', None), float),
            'swimming_num_strokes_float': convert_to_type(
                _data.get('swimming_num_strokes_number', None), float),
            'swimming_num_laps_int': convert_to_type(
                _data.get('swimming_num_laps_number', None), int),
            'swimming_pool_length_meters_float': convert_to_type(
                _data.get('swimming_pool_length_meters', None), float),
            'swimming_total_distance_meters_float': convert_to_type(
                _data.get('swimming_total_distance_meters', None), float),
            'elevation_granular_data_array': GranularData.elevation_granular_data(
                _data, 'elevation_granular_data_meters'),
            'floors_climbed_granular_data_array': GranularData.floors_climbed_granular_data(
                _data, 'floors_climbed_granular_data_floors_number'),
            'traveled_distance_granular_data_array': GranularData.traveled_granular_data(
                _data, 'traveled_distance_granular_data_meters'),
            'steps_granular_data_array': GranularData.steps_granular_data(
                _data, 'steps_granular_data_steps_per_min'),
            'swimming_distance_granular_data_array': GranularData.swimming_granular_data(
                _data, 'swimming_distance_granular_data_meters')
            }

    @classmethod
    def movement_data(cls, _data: dict) -> dict:

        velocity_avg_array = GranularData.velocity_granular_data(
            _data, 'velocity_vector_avg_speed_and_direction')

        if velocity_avg_array:
            velocity_avg_object = velocity_avg_array
        else:
            velocity_avg_object = {
                'speed_meters_per_second_float': None,
                'direction_string': None
                }

        velocity_max_array = GranularData.velocity_granular_data(
            _data, 'velocity_vector_max_speed_and_direction'
            )

        if velocity_max_array:
            velocity_max_object = velocity_max_array
        else:
            velocity_max_object = {
                'speed_meters_per_second_float': None,
                'direction_string': None
                }

        return {
            'speed_normalized_meters_per_second_float': convert_to_type(
                _data.get('speed_normalized_meters_per_second', None), float),
            'speed_avg_meters_per_second_float': convert_to_type(
                _data.get('speed_avg_meters_per_second', None), float),
            'speed_maximum_meters_per_second_float': convert_to_type(
                _data.get('speed_max_meters_per_second', None), float),
            'pace_avg_min_per_km_float': convert_to_type(
                _data.get('pace_avg_minutes_per_kilometer', None), float),
            'pace_maximum_min_per_km_float': convert_to_type(
                _data.get('pace_max_minutes_per_kilometer', None), float),
            'cadence_avg_rpm_float': convert_to_type(_data.get('cadence_avg_rpm', None), float),
            'cadence_maximum_rpm_float': convert_to_type(
                _data.get('cadence_max_rpm', None), float),
            'torque_avg_newton_meters_float': convert_to_type(
                _data.get('torque_avg_newton_meters', None), float),
            'torque_maximum_newton_meters_float': convert_to_type(
                _data.get('torque_max_newton_meters', None), float),
            'velocity_avg_object': velocity_avg_object,
            'velocity_maximum_object': velocity_max_object,
            'cadence_granular_data_array': GranularData.cadence_granular_data(
                _data, 'cadence_granular_data_rpm'),
            'lap_granular_data_array': GranularData.lap_granular_data(
                _data, 'lap_granular_data_laps_number'),
            'speed_granular_data_array': GranularData.speed_granular_data(
                _data, 'speed_granular_data_meters_per_second'),
            'torque_granular_data_array': GranularData.torque_granular_data(
                _data, 'torque_granular_data_newton_meters'
                )
            }

    @classmethod
    def power_data(cls, _data: dict) -> dict:

        return {
            'power_avg_watts_float': convert_to_type(
                _data.get('power_avg_watts_number', None), float),
            'power_maximum_watts_float': convert_to_type(
                _data.get('power_max_watts_number', None), float),
            'power_granular_data_array': GranularData.power_granular_data(
                _data, 'power_granular_data_watts_number')
            }

    @classmethod
    def position_data(cls, _data: dict) -> dict:

        position_start_array = GranularData.position_granular_data(
            _data, 'position_start_lat_lng_deg', True)

        if position_start_array:
            position_start_object = position_start_array
        else:
            position_start_object = {
                'lat_deg_float': None,
                'lng_deg_float': None
                }

        position_centroid_array = GranularData.position_granular_data(
            _data, 'position_centroid_lat_lng_deg', True)

        if position_centroid_array:
            position_centroid_object = position_centroid_array
        else:
            position_centroid_object = {
                'lat_deg_float': None,
                'lng_deg_float': None
                }

        position_end_array = GranularData.position_granular_data(
            _data, 'position_end_lat_lng_deg', True)

        if position_end_array:
            position_end_object = position_end_array
        else:
            position_end_object = {
                'lat_deg_float': None,
                'lng_deg_float': None
                }

        return {
            'position_start_object': position_start_object,
            'position_centroid_object': position_centroid_object,
            'position_end_object': position_end_object,
            'position_granular_data_array': GranularData.position_granular_data(
                _data, 'position_granular_data_lat_lng_deg'),
            'position_polyline_map_data_summary_string': convert_to_type(
                _data.get('position_polyline_map_data_summary_string', None), str)
            }


build_json = ActivityEvents.build_json

__all__ = ['build_json']
