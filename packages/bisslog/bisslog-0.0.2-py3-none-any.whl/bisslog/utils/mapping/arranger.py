"""Implementation of the primitive data arranger"""
import re
from datetime import datetime
from abc import ABC
from typing import Optional, Any


class IArranger(ABC):
    """Arranger interface in charge of processing primitive data by type

    Example
    -------
    arrangeData("420.4", dtype="number", defaultValue=100) -> 420.4
    arrangeData("", dtype="number", defaultValue=100) -> 100
    arrangeData("", dtype="number") -> None
    """

    datetime_processors = {
        "iso": lambda x: x.isoformat(),
        "year": lambda x: x.year,
        "day": lambda x: x.day,
        "month": lambda x: x.month,
        "weekday": lambda x: x.weekday(),
        "hour": lambda x: x.hour,
        "minute": lambda x: x.minute,
        "timestamp": lambda x: x.timestamp(),
        "time": lambda x: x.time(),
        "date": lambda x: x.date(),
        "fold": lambda x: x.fold,
    }

    def __init__(self):
        self.__processors = {
            # datetime
            "datetime": self.__process_datetime,
            "date": self.__process_datetime,
            # string
            "string": self.__process_string,
            "str": self.__process_string,
            # numbers
            "number": self.__process_number,
            "float": self.__process_number,
            "decimal": self.__process_number,

            "integer": self.__process_integer,
            "int": self.__process_integer,

            # enum
            "enum": self.__process_enum,

            # no type
            "-": self.__process_not_type
        }

    @staticmethod
    def process_datetime_when_is_string(value, date_format = "iso") -> Optional[datetime]:
        res = None
        if date_format == "iso":
            try:
                res = datetime.fromisoformat(value)
            except ValueError:
                pass  # res = None
        elif date_format == "timestamp" and value.replace(".", "", 1).isdigit():
            res = datetime.fromtimestamp(float(value))
        else:
            try:
                res = datetime.strptime(value, date_format)
            except ValueError:
                pass
        return res

    @staticmethod
    def __process_datetime(value, date_format="iso", default_value=None, transform=None, *_, **__):
        """Valid and formats if possible the value in a datetime as handled by events,
        otherwise returns None

        Parameters
        ----------
        value: object
            expected to be of type datetime

        Returns
        -------
        datetime: Object datetime
        """
        res = None
        if isinstance(value, datetime):
            res = value
        elif isinstance(value, (float, int)):
            res = datetime.fromtimestamp(value)
        elif isinstance(value, str):
            res = IArranger.process_datetime_when_is_string(value, date_format)
        elif default_value == "now":
            res = datetime.now()

        if transform is not None and isinstance(res, datetime):
            res = IArranger.datetime_processors.get(transform, lambda x: x)(res)
        elif isinstance(res, datetime):
            res = res.timestamp()
        return res

    @staticmethod
    def __process_enum(value, enum, *_, **__):
        """Valid and formats if possible the value in a datetime as handled by events,
        otherwise returns None

        Parameters
        ----------
        value: object
            expected to be of type enum

        Returns
        -------
        object: Object on enum
        """
        if value in enum:
            return value
        return None

    @staticmethod
    def __process_string(value, *_, **__) -> str:
        """Valid and formats if possible the value in a string as handled by events,
        otherwise returns None

        Parameters
        ----------
        value: object
            expected to be of type string

        Returns
        -------
        str: Object string
        """
        return str(value)

    @staticmethod
    def __process_integer(value, *_, **__) -> Optional[int]:
        """Valid and formats if possible the value in an integer as handled by events,
        otherwise returns None

        Parameters
        ----------
        value: object
            expected to be of type integer

        Returns
        -------
        str, optional: Object integer
        """
        if isinstance(value, int):
            return value
        if (isinstance(value, str) and re.fullmatch(r"\d+\.?0*", value)) or \
                isinstance(value, bool):
            return int(float(value))
        return None

    @staticmethod
    def __process_number(value, *_, **__) -> Optional[float]:
        """Valid and formats if possible the value in an integer as handled by events,
        otherwise returns None

        Parameters
        ----------
        value: object
            expected to be of type integer

        Returns
        -------
        str, optional: Object integer
        """
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            if value.isdigit():
                return int(value)
            if value.replace(".", "", 1).isdigit():
                return float(value)
        return None

    @staticmethod
    def __process_not_type(value, *_, **__):
        """Valid and formats if possible the value in an integer as handled by events,
        otherwise returns None

        Parameters
        ----------
        value: object
            expected to be of non type

        Returns
        -------
        str, optional: same object as value
        """
        return value

    def arrange_value(self, value, dtype: str= "-", default_value=None, *args, **kwargs) -> Any:
        """Organizes a value according to type and prevents it from remaining as a None.

        Parameters
        ----------
        value: object
            Value with primitive payload
        dtype: str, optional
            Valid data type
        default_value: object
            Default object to be imposed if it is set as None

        Returns
        -------
        object: Arranged value
        """
        if dtype in self.__processors and value is not None:
            _process = self.__processors[dtype]
            res = _process(value, defaultValue=default_value, *args, **kwargs)
            if res is not None:
                return res
        return default_value
