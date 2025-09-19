from abc import ABC, abstractmethod

class BusinessRule(ABC):
    __message: str = "The business rule is invalid"

    def __init__(self, message: str):
        self.__message = message

    def error_message(self) -> str:
        return self.__message

    @abstractmethod
    def is_valid(self) -> bool:
        ...

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - {self.__message}"