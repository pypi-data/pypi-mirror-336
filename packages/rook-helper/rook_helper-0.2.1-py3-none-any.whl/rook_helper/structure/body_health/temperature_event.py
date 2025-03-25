from rook_helper.structure import StructureBase, GranularData


class TemperatureEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'temperature_event'
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
            'temperature': cls.temperature_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def temperature_data(cls, _data: dict) -> dict:

        temperature_avg_celsius = GranularData.temperature_granular_data(
            _data, 'temperature_avg_celsius', True)

        if temperature_avg_celsius:
            temperature_avg_celsius_object = temperature_avg_celsius
        else:
            temperature_avg_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_max_celsius = GranularData.temperature_granular_data(
            _data, 'temperature_max_celsius', True)

        if temperature_max_celsius:
            temperature_max_object = temperature_max_celsius
        else:
            temperature_max_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_min_celsius = GranularData.temperature_granular_data(
            _data, 'temperature_minimum_celsius', True)

        if temperature_min_celsius:
            temperature_min_celsius_object = temperature_min_celsius
        else:
            temperature_min_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_delta_celsius = GranularData.temperature_granular_data(
            _data, 'temperature_delta_celsius', True)

        if temperature_delta_celsius:
            temperature_delta_celsius_object = temperature_delta_celsius
        else:
            temperature_delta_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        return {
            'temperature_avg_object': temperature_avg_celsius_object,
            'temperature_maximum_object': temperature_max_object,
            'temperature_minimum_object': temperature_min_celsius_object,
            'temperature_delta_object': temperature_delta_celsius_object,
            'temperature_granular_data_array': GranularData.temperature_granular_data(
                _data, 'temperature_granular_data_celsius')
            }


build_json = TemperatureEvent.build_json

__all__ = ['build_json']
