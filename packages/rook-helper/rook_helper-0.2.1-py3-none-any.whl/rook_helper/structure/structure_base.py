from rook_helper import remove_client_uuid_from_user_id, format_datetime


class StructureBase:

    _expected_data_structure = {
        'pillar': str,
        'data_structure_type': str,
        'data_type': str | None,
        'client_uuid': str,
        'user_id': str,
        'document_version': int,
        'auto_detected': bool
        }

    _expected_metadata = {
        'client_uuid': str,
        'user_id': str,
        'datetime': str,
        'sources_of_data': str | list,
        'was_the_user_under_physical_activity': bool
        }

    @classmethod
    def build_data_structure(cls, **_data) -> dict:

        validate, message = cls.validate_data_structure(_data, cls._expected_data_structure, True)

        if not validate:
            raise ValueError(message)

        data_structure = {
            'version': 2,
            'data_structure': _data.get('data_structure_type'),
            'client_uuid': _data.get('client_uuid'),
            'user_id': _data.get('user_id'),
            'document_version': _data.get('document_version')
            }

        data_type = _data.get('data_type')
        pillar = _data.get('pillar')

        if data_type == 'events':
            data_structure['auto_detected'] = _data.get('auto_detected')

        pillar_mapping = {
            'physical_health': 'physical_health',
            'body_health': 'body_health',
            'sleep_health': 'sleep_health',
            'user_information': 'user_information'
            }

        if pillar not in pillar_mapping:
            raise ValueError(f'The pillar does not exist: {pillar}')

        data_structure[pillar_mapping[pillar]] = {}

        if pillar != 'user_information':
            subcategory = 'events' if data_type == 'events' else 'summary'
            data_structure[pillar_mapping[pillar]][subcategory] = {}  # type: ignore
        else:
            data_structure['user_information']['user_body_metrics'] = {}  # type: ignore
            data_structure['user_information']['user_demographics'] = {}  # type: ignore

        return data_structure

    @classmethod
    def build_metadata(cls, **_data) -> dict:

        validate, message = cls.validate_data_structure(_data, cls._expected_metadata)

        if not validate:
            raise ValueError(message)

        client_uuid = _data.get('client_uuid', '')
        user_id = _data.get('user_id', '')

        metadata = {
            'datetime_string': format_datetime(_data.get('datetime', '')),
            'user_id_string': remove_client_uuid_from_user_id(user_id, client_uuid),
            'sources_of_data_array': _data.get('sources_of_data'),
            'was_the_user_under_physical_activity_bool': _data.get(
                'was_the_user_under_physical_activity')
            }

        return metadata

    @staticmethod
    def validate_data_structure(_data: dict,
                                expected_structure: dict,
                                document_version: bool = False) -> tuple:

        missing_keys = [
            key for key in expected_structure
            if key not in _data or (isinstance(_data[key], str) and not _data[key].strip())]

        if missing_keys:
            return False, f'The following keys are missing or have empty values: {missing_keys}'

        incorrect_types = {
            key: (type(_data[key]), expected_structure[key])
            for key in expected_structure
            if not isinstance(_data[key], expected_structure[key])
            }

        if incorrect_types:
            return False, f'Data type errors: {incorrect_types}'

        if document_version and _data['document_version'] <= 0:
            return False, 'document_version must be a positive number'

        return True, None
