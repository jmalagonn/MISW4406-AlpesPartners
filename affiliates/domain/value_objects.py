from dataclasses import dataclass
import re
import uuid

@dataclass(frozen=True)
class ValueObject:
    ...

@dataclass(frozen=True)
class Email(ValueObject):
    address: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.address):
            raise ValueError(f"Invalid email: {self.address}")

@dataclass(frozen=True)
class ProgramId(ValueObject):
    id: uuid.UUID