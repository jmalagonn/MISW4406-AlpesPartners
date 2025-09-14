from infrastructure.db.db import session_scope
from domain.factory import InteractionFactory, InteractionMapper
from infrastructure.event_store.postgresql_event_store import PostgreSQLEventStore
from infrastructure.projections.projection_handler import ProjectionHandler


class InteractionHandler:
    """
    Handler que usa Event Sourcing para procesar comandos
    """
    
    def __init__(self):
        self.factory = InteractionFactory()
        self.mapper = InteractionMapper()
    
    def handle_track_interaction(self, data: dict) -> str:
        """
        Maneja el comando de trackear interacción usando Event Sourcing
        """
        try:
            print("Handler: Creando entidad...")
            interaction = self.factory.create_object(data, self.mapper)
            print("Handler: Entidad creada exitosamente")

            print("Handler: Abriendo sesión de BD...")
            with session_scope() as session:
                print("Handler: Guardando eventos en Event Store...")
                event_store = PostgreSQLEventStore(session)
                event_store.save_events(
                    aggregate_id=interaction.id,
                    events=interaction.events,
                    expected_version=0 
                )
                print("Handler: Eventos guardados exitosamente")
                
                print("Handler: Procesando proyecciones...")
                projection_handler = ProjectionHandler(session)
                for event in interaction.events:
                    projection_handler.handle_event(event)
                print("Handler: Proyecciones procesadas exitosamente")
            
            print(f"Handler: Retornando ID: {str(interaction.id)}")
            return str(interaction.id)
            
        except Exception as e:
            print(f"Error en handler: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise
