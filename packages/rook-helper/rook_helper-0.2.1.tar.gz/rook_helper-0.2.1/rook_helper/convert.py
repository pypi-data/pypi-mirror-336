from typing import Type, TypeVar, Union, Optional

T = TypeVar('T', int, float, str, bool)


def convert_to_type(_value: Union[str, float, int, bool],
                    _data_type: Type[T]) -> Optional[T]:

    if _value is None:
        return None

    if _data_type is bool:
        if isinstance(_value, bool):
            return _value  # type: ignore
        return None

    if _data_type is str and _value == '':
        return None

    try:
        return _data_type(_value)
    except (ValueError, TypeError):
        return None
