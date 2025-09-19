import uuid
from dataclasses import dataclass
from alliances.application.dto import CreatePaymentOrderDTO
from alliances.infrastructure.factories.factory_repository import FactoryRepository
from seedwork.application.commands import Command, CommandHandler


@dataclass
class CreatePaymentOrder(Command):
    start_date: str
    end_date: str
    post_id: uuid
    

class CreatePaymentOrderHandler(CommandHandler):
    def __init__(self):
        self.factory_repository: FactoryRepository = FactoryRepository()
        
    def handle(self, command: CreatePaymentOrder):
        print(f"Handling CreatePaymentOrder command: {command}")
      
        create_payment_order_dto = CreatePaymentOrderDTO(
          start_date=command.start_date,
          end_date=command.end_date,
          post_id=str(command.post_id)
        )
        
        
        
        
  
    

