"""Módulo para el mapeo y transformación de parámetros de entrada."""
from typing import Union

from .mapping_group import MappingGroup
from .arranger import IArranger
from .mapper import Mapper



def build_mapper(mappers = None) -> Union[MappingGroup, Mapper]:
    mapper_ = None
    if mappers:
        if isinstance(mappers, (list, tuple)):
            mapper_ = MappingGroup(
                [Mapper("", i) if isinstance(i, dict) else i for i in mappers])
        elif isinstance(mappers, dict):
            mapper_ = Mapper("Http mapper_", mappers)
        elif isinstance(mappers, (MappingGroup, Mapper)):
            mapper_ = mappers
        else:
            raise TypeError("Invalid mapper type")
    return mapper_


__all__ = ["MappingGroup", "Mapper", "IArranger", "build_mapper"]
