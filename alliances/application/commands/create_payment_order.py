import uuid
from dataclasses import dataclass
from alliances.application.dto import CreatePaymentOrderDTO
from seedwork.application.commands import Command, CommandHandler


@dataclass
class CreatePaymentOrder(Command):
    start_date: str
    end_date: str
    post_id: uuid
    

class CreatePaymentOrderHandler(CommandHandler):
    def handle(self, command: CreatePaymentOrder):
        print(f"Handling CreatePaymentOrder command: {command}")
      
        create_payment_order_dto = CreatePaymentOrderDTO(
  
    

