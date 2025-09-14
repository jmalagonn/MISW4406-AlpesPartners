from infrastructure.repository import InteractionRepository
from infrastructure.db.db import session_scope
from application.factories.interaction_factory import InteractionFactory, InteractionMapper


class InteractionHandler:
    """
    Handler que usa la factory para procesar comandos
    """
    
    def __init__(self):
        self.factory = InteractionFactory()
        self.mapper = InteractionMapper()
    
    def handle_track_interaction(self, data: dict) -> str:
        """
        Maneja el comando de trackear interacción
        """
        try:
            print("Handler: Creando entidad...")
            interaction = self.factory.create_object(data, self.mapper)
            print("Handler: Entidad creada exitosamente")

            print("Handler: Abriendo sesión de BD...")
            with session_scope() as session:
                print("Handler: Creando repositorio...")
                repo = InteractionRepository(session)
                print("Handler: Agregando entidad al repositorio...")
                repo.add(interaction)
                print("Handler: Entidad agregada exitosamente")
            
            print(f"Handler: Retornando ID: {str(interaction.id)}")
            return str(interaction.id)
            
        except Exception as e:
            print(f"Error en handler: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise
