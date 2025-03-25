from datetime import datetime, timezone
from uuid import UUID


def format_datetime(_datetime: str | None) -> str | None:

    if _datetime is None:
        return None

    try:
        parsed_datetime = datetime.fromisoformat(_datetime)
    except ValueError as e:
        raise e

    if parsed_datetime.tzinfo is None:
        parsed_datetime = parsed_datetime.replace(tzinfo=timezone.utc)

    formatted_datetime = parsed_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    formatted_datetime = f'{formatted_datetime[:-2]}:{formatted_datetime[-2:]}'

    return formatted_datetime.replace('+00:00', 'Z')


def remove_client_uuid_from_user_id(_user_id: str, _client_uuid: str) -> str:
    if not _user_id or not _user_id.strip():
        raise ValueError('The provided user_id is empty or None.')

    if not _is_valid_uuid(_client_uuid):
        raise ValueError('Invalid client_uuid: must be a valid UUIDv4.')

    client_uuid_prefix = _client_uuid.split('-')[0]

    if client_uuid_prefix not in _user_id:
        raise ValueError('Mismatch: The client_uuid prefix does not match the user_id.')

    user_id_part = _user_id.split('-')
    new_user_id = '-'.join(user_id_part[:-1])

    return new_user_id


def _is_valid_uuid(_client_uuid: str) -> bool:

    try:
        return str(UUID(_client_uuid, version=4)) == _client_uuid
    except Exception:
        return False
