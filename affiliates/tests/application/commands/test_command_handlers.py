import uuid
from types import SimpleNamespace
import pytest

import application.commands.command_handlers as ch
from domain.value_objects import Name


class FakeSession:
    def __init__(self):
        self.added = []
        self.by_id = {}


class FakeRepo:
    def __init__(self, session):
        self.session = session

    def add(self, entity):
        self.session.added.append(entity)
        self.session.by_id[getattr(entity, "id")] = entity

    def get(self, entity_id):
        return self.session.by_id.get(entity_id)


class FakeAffiliate:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self._renamed_to = None

    def rename(self, new_name: str):
        self._renamed_to = new_name


# ------------------------------ Tests -----------------------------------
def test_handle_create_affiliate_happy_path(monkeypatch):
    # Arrange
    session = FakeSession()
    cmd = SimpleNamespace(name="  Afiliado 1  ")

    # Inyectamos fakes en el módulo bajo prueba
    monkeypatch.setattr(ch, "AffiliateRepository", FakeRepo)
    monkeypatch.setattr(ch, "Affiliate", FakeAffiliate)

    # Act
    new_id = ch.handle_create_affiliate(cmd, session)

    # Assert
    # 1) Se devolvió un UUID
    assert isinstance(new_id, uuid.UUID)

    # 2) Se agregó exactamente una entidad al "repositorio"
    assert len(session.added) == 1
    saved = session.added[0]

    # 3) La entidad recibió un Name VO con el nombre ya "limpio"
    assert isinstance(saved.name, Name)
    assert saved.name.name == "Afiliado 1"  # sin espacios extremos


def test_handle_rename_affiliate_happy_path(monkeypatch):
    # Arrange
    session = FakeSession()
    monkeypatch.setattr(ch, "AffiliateRepository", FakeRepo)

    existing = FakeAffiliate(name=Name("Viejo Nombre"))
    session.by_id[existing.id] = existing

    cmd = SimpleNamespace(id=existing.id, name="Nuevo Nombre")

    # Act
    ch.handle_rename_affiliate(cmd, session)

    # Assert: el método rename fue llamado con el valor correcto
    assert existing._renamed_to == "Nuevo Nombre"


def test_handle_rename_affiliate_not_found(monkeypatch):
    # Arrange
    session = FakeSession()
    monkeypatch.setattr(ch, "AffiliateRepository", FakeRepo)

    cmd = SimpleNamespace(id=uuid.uuid4(), name="Nuevo Nombre")

    # Act & Assert
    with pytest.raises(ValueError) as exc:
        ch.handle_rename_affiliate(cmd, session)

    assert "Affiliate not found" in str(exc.value)
