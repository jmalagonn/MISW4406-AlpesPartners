from abc import ABC, abstractmethod
from .mixins import ValidateRulesMixin
from .repositories import Mapper


class Factory(ABC, ValidateRulesMixin):
    @abstractmethod
    def create_object(self, obj: any, mapeador: Mapper=None) -> any:
        ...