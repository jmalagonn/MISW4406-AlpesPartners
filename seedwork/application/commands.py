from abc import ABC, abstractmethod


class Command:
  ...
  

class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command):
        raise NotImplementedError()