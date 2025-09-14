from typing import List
import uuid
import json
from datetime import datetime
from sqlalchemy.orm import Session
from seedwork.domain.event_store import EventStore, Event

class UUIDEncoder(json.JSONEncoder):
    """
    Encoder personalizado para manejar UUID y datetime en JSON
    """
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class PostgreSQLEventStore(EventStore):
    """
    Implementación del Event Store usando PostgreSQL
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def save_events(self, aggregate_id: uuid.UUID, events: List[Event], expected_version: int) -> None:
        """
        Guarda eventos para un aggregate
        """

        current_version = self._get_current_version(aggregate_id)
        if current_version != expected_version:
            raise ValueError(f"Expected version {expected_version}, but current version is {current_version}")
        
        
        for event in events:
            event.created_at = datetime.now()
            self._save_event(event)
    
    def get_events(self, aggregate_id: uuid.UUID) -> List[Event]:
        """
        Obtiene todos los eventos de un aggregate
        """
        from infrastructure.db.db_models import EventModel
        
        event_models = self.session.query(EventModel).filter(
            EventModel.aggregate_id == aggregate_id
        ).order_by(EventModel.version).all()
        
        events = []
        for event_model in event_models:
            event_class = self._get_event_class(event_model.event_type)
            event_data = json.loads(event_model.event_data)
            
            # Convertir strings de UUID y datetime de vuelta a sus tipos originales
            if 'interaction_id' in event_data:
                event_data['interaction_id'] = uuid.UUID(event_data['interaction_id'])
            if 'aggregate_id' in event_data:
                event_data['aggregate_id'] = uuid.UUID(event_data['aggregate_id'])
            if 'timestamp' in event_data:
                event_data['timestamp'] = datetime.fromisoformat(event_data['timestamp'])
            
            event = event_class(**event_data)
            events.append(event)
        
        return events
    
    def _save_event(self, event: Event) -> None:
        """
        Guarda un evento individual
        """
        from infrastructure.db.db_models import EventModel
        
        event_model = EventModel(
            id=uuid.uuid4(),
            aggregate_id=event.aggregate_id,
            event_type=event.__class__.__name__,
            event_data=json.dumps(event.__dict__, cls=UUIDEncoder),
            version=event.version,
            created_at=event.created_at,
            event_metadata=None
        )
        
        self.session.add(event_model)
    
    def _get_current_version(self, aggregate_id: uuid.UUID) -> int:
        """
        Obtiene la versión actual de un aggregate
        """
        from infrastructure.db.db_models import EventModel
        
        result = self.session.query(EventModel).filter(
            EventModel.aggregate_id == aggregate_id
        ).order_by(EventModel.version.desc()).first()
        
        return result.version if result else 0
    
    def _get_event_class(self, event_type: str):
        """
        Obtiene la clase del evento por su tipo
        """

        from domain.events import InteractionTracked
        
        event_classes = {
            'InteractionTracked': InteractionTracked
        }
        
        return event_classes.get(event_type)
