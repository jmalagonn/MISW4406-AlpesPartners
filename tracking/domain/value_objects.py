from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    ...
    
    
@dataclass(frozen=True)
class Name(ValueObject):
    name: str
    
    def __str__(self): 
        return self.name


@dataclass(frozen=True)
class InteractionType(ValueObject):
    value: str
    
    def __post_init__(self):
        valid_types = ['click', 'view', 'like']
        if self.value not in valid_types:
            raise ValueError(f"Invalid interaction type: {self.value}")
    
    def __str__(self):
        return self.value


@dataclass(frozen=True)
class TargetElement(ValueObject):
    element_id: str
    element_type: str  # button, product, page, etc.
    
    def __str__(self):
        return f"{self.element_type}:{self.element_id}"


@dataclass(frozen=True)
class CampaignId(ValueObject):
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("Campaign ID cannot be empty")
    
    def __str__(self):
        return self.value