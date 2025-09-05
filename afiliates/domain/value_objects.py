from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    ...
    
    
@dataclass(frozen=True)
class Name(ValueObject):
    name: str