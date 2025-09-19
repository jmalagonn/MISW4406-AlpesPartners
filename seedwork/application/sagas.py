from dataclasses import dataclass
import datetime, uuid
from abc import ABC, abstractmethod
from seedwork.application.commands import Command, execute_command
from seedwork.domain.events import DomainEvent


class SagaCoordinator(ABC):
    id_correlacion: uuid.UUID

    @abstractmethod
    def add_to_saga_log(self, mensaje):
        ...

    @abstractmethod
    def build_command(self, event: DomainEvent, command_type: type) -> Command:
        ...

    def publish_command(self, event: DomainEvent, command_type: type):
        command = build_command(event, command_type)
        execute_command(command)

    @abstractmethod
    def init_steps(self):
        ...
    
    @abstractmethod
    def process_event(self, event: DomainEvent):
        ...

    @abstractmethod
    def init():
        ...
    
    @abstractmethod
    def finish():
        ...
        

class Step():
    corr_id: uuid.UUID
    created_at: datetime.datetime
    index: int
    
    
@dataclass
class Start(Step):
    index: int = 0
    
    
@dataclass
class End(Step):
    ...
    
    
@dataclass
class Transaction(Step):
    
    command: Command
    event: DomainEvent
    error: DomainEvent
    compensation: Command
    isSuccessfull: bool
    
    
class SagaCoordinator(SagaCoordinator, ABC):
    ...
    
    
class OrchestrationCoordinator(SagaCoordinator, ABC):
    steps: list["Step"]
    index: int

    def get_step_given_event(self, event: "DomainEvent"):
        for i, step in enumerate(self.steps):
            if not isinstance(step, Transaction):
                continue

            if isinstance(event, step.event) or isinstance(event, step.error):
                return step, i
        raise Exception("Event is not part of the transaction")

    def is_last_transaction(self, index: int) -> bool:
        return index == len(self.steps) - 1

    def process_event(self, event: "DomainEvent"):
        step, index = self.get_step_given_event(event)

        if self.is_last_transaction(index) and not isinstance(event, step.error):
            self.finish()
        elif isinstance(event, step.error):
            self.publish_command(event, self.steps[index - 1].compensation)
        elif isinstance(event, step.event):
            self.publish_command(event, self.steps[index + 1].compensation)
    
    

    

