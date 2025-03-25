from rook_helper import convert_to_type, format_datetime


class GranularData:

    @classmethod
    def activity_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'activity_level' not in item:
                continue

            new_item = {
                'activity_level_float': convert_to_type(item.get('activity_level', None), float),
                'activity_level_label_string': convert_to_type(
                    item.get('activity_level_label_string', None), str),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def blood_glucose_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'blood_glucose_mg_per_dL' not in item:
                continue

            new_item = {
                'blood_glucose_mg_per_dL_int': convert_to_type(
                    item.get('blood_glucose_mg_per_dL', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def blood_pressure_granular_data(cls,
                                     _data: dict,
                                     _variable: str,
                                     _object: bool = False) -> list | dict:

        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            is_dict = isinstance(item, dict)
            missing_keys = 'systolic_bp' not in item and 'diastolic_bp' not in item

            if is_dict and missing_keys:
                continue

            new_item = {
                'diastolic_mmHg_int': convert_to_type(item.get('diastolic_bp', None), int),
                'systolic_mmHg_int': convert_to_type(item.get('systolic_bp', None), int)
                }

            if not _object:
                new_item.update({
                    'datetime_string': format_datetime(item.get('datetime', None)),   # type: ignore
                    'interval_duration_seconds_float': convert_to_type(  # type: ignore
                        item.get('interval_duration_seconds', None), float)
                    })

            processed_data.append(new_item)

        if _object:
            return {k: v for d in processed_data for k, v in d.items()}  # type: ignore

        return processed_data

    @classmethod
    def breathing_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'breaths_per_min' not in item:
                continue

            new_item = {
                'breaths_per_min_int': convert_to_type(item.get('breaths_per_min', None), int),
                'datetime_string': format_datetime(item.get('datetime', None))
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def elevation_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'elevation_change' not in item:
                continue

            new_item = {
                'elevation_change_meters_float': convert_to_type(
                    item.get('elevation_change', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def floors_climbed_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'floors_climbed' not in item:
                continue

            new_item = {
                'floors_climbed_float': convert_to_type(item.get('floors_climbed', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def menstruation_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'flow_ml' not in item:
                continue

            new_item = {
                'flow_mL_int': convert_to_type(item.get('flow_ml', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def heart_rate_granular_data(cls,
                                 _data: dict,
                                 _granular_data: str,
                                 _variable: str,
                                 _new_variable: str,
                                 _float_type: bool = True,) -> list:

        granular_data = _data.get(_granular_data, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or _variable not in item:
                continue

            new_item = {
                _new_variable: convert_to_type(item[_variable], float if _float_type else int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def hydration_granular_data(cls,
                                _data: dict,
                                _granular_data: str,
                                _variable: str,
                                _new_variable: str) -> list:

        granular_data = _data.get(_granular_data, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or _variable not in item:
                continue

            new_item = {
                _new_variable: convert_to_type(item[_variable], int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def mood_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'mood_scale' not in item:
                continue

            new_item = {
                'mood_scale_int': convert_to_type(item['mood_scale'], int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def temperature_granular_data(cls,
                                  _data: dict,
                                  _variable: str,
                                  _object: bool = False) -> list | dict:

        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'temperature_celsius' not in item:
                continue

            new_item = {
                'temperature_celsius_float': convert_to_type(
                    item.get('temperature_celsius', None), float),
                'measurement_type_string': convert_to_type(
                    item.get('measurement_type', None), str),
                }

            if not _object:
                new_item.update({
                    'datetime_string': format_datetime(item.get('datetime', None)),
                    'interval_duration_seconds_float': convert_to_type(
                        item.get('interval_duration_seconds', None), float)
                    })

            processed_data.append(new_item)

        if _object:
            return {k: v for d in processed_data for k, v in d.items()}  # type: ignore

        return processed_data

    @classmethod
    def saturation_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'saturation_percentage' not in item:
                continue

            new_item = {
                'saturation_percentage_int': convert_to_type(
                    item.get('saturation_percentage', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def snoring_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'snoring_events_count_number' not in item:
                continue

            new_item = {
                'snoring_events_count_int': convert_to_type(
                    item.get('snoring_events_count_number', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def steps_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'steps' not in item:
                continue

            new_item = {
                'steps_int': convert_to_type(item.get('steps', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def active_steps_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'steps' not in item:
                continue

            new_item = {
                'steps_int': convert_to_type(item.get('steps', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def stress_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'stress_score' not in item:
                continue

            new_item = {
                'stress_score_int': convert_to_type(item.get('stress_score', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def swimming_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'swimming_distance_meters' not in item:
                continue

            new_item = {
                'swimming_distance_meters_float':  convert_to_type(
                    item.get('swimming_distance_meters', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def traveled_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'traveled_distance_meters' not in item:
                continue

            new_item = {
                'traveled_distance_meters_float': convert_to_type(
                    item.get('traveled_distance_meters', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def tss_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'tss_1_500_score' not in item:
                continue

            new_item = {
                'tss_score_int': convert_to_type(item.get('tss_1_500_score', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def vo2_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'vo2_ml_per_min' not in item:
                continue

            new_item = {
                'vo2_mL_per_min_per_kg_int': convert_to_type(
                    item.get('vo2_ml_per_min', None), int),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def cadence_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'cadence_rpm' not in item:
                continue

            new_item = {
                'cadence_rpm_float': convert_to_type(item.get('cadence_rpm', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def lap_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'laps' not in item:
                continue

            new_item = {
                'laps_int': convert_to_type(item.get('laps', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def speed_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'speed_meters_per_second' not in item:
                continue

            new_item = {
                'speed_meters_per_second_float': convert_to_type(
                    item.get('speed_meters_per_second', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def torque_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'torque_newton_meters' not in item:
                continue

            new_item = {
                'torque_newton_meters_float': convert_to_type(
                    item.get('torque_newton_meters', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def velocity_granular_data(cls, _data: dict, _variable: str) -> dict | list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'speed_meters_per_second' not in item:
                continue

            new_item = {
                'speed_meters_per_second_float': convert_to_type(
                    item.get('speed_meters_per_second', None), float),
                'direction_string': format_datetime(item.get('datetime', None))
                }

            processed_data.append(new_item)

        return {k: v for d in processed_data for k, v in d.items()}  # type: ignore

    @classmethod
    def power_granular_data(cls, _data: dict, _variable: str) -> list:
        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'power_watts' not in item:
                continue

            new_item = {
                'power_watts_float': convert_to_type(
                    item.get('power_watts', None), float),
                'datetime_string': format_datetime(item.get('datetime', None)),
                'interval_duration_seconds_float': convert_to_type(
                    item.get('interval_duration_seconds', None), float)
                }

            processed_data.append(new_item)

        return processed_data

    @classmethod
    def position_granular_data(cls,
                               _data: dict,
                               _variable: str,
                               _object: bool = False) -> list | dict:

        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            is_dict = isinstance(item, dict)
            missing_keys = 'lat' not in item and 'lng' not in item

            if is_dict and missing_keys:
                continue

            new_item = {
                'lat_deg_float': convert_to_type(item.get('lat', None), float),
                'lng_deg_float': convert_to_type(item.get('lng', None), float)
                }

            if not _object:
                new_item.update({
                    'datetime_string': format_datetime(item.get('datetime', None)),  # type: ignore
                    'interval_duration_seconds_float': convert_to_type(
                        item.get('interval_duration_seconds', None), float)
                    })

            processed_data.append(new_item)

        if _object:
            return {k: v for d in processed_data for k, v in d.items()}  # type: ignore

        return processed_data
