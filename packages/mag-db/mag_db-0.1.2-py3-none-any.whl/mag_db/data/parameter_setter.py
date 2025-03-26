from dataclasses import field
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, List, Tuple

from pydantic.dataclasses import dataclass


@dataclass
class ParameterSetter:
    __parameter_cache: List[Any] = field(default_factory=list)

    def get_values(self)->Tuple[Any,...]:
        return tuple(self.__parameter_cache)

    def set_string(self, parameter: str):
        self.__parameter_cache.append(parameter)

    def set_int(self, parameter: int):
        self.__parameter_cache.append(parameter)

    def set_bool(self, parameter: bool):
        self.__parameter_cache.append(parameter)

    def set_float(self, parameter: float):
        self.__parameter_cache.append(parameter)

    def set_decimal(self, parameter: Decimal):
        self.__parameter_cache.append(parameter)

    def set_bytes(self, parameter: bytes):
        self.__parameter_cache.append(parameter)

    def set_date(self, parameter: date):
        self.__parameter_cache.append(parameter)

    def set_time(self, parameter: time):
        self.__parameter_cache.append(parameter)

    def set_date_time(self, parameter: datetime):
        self.__parameter_cache.append(parameter)

    def set_url(self, parameter: str):
        self.__parameter_cache.append(parameter)