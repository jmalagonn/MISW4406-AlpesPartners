from dataclasses import dataclass

@dataclass
class CreateAfiliate:
    name: str

@dataclass
class RenameAfiliate:
    afiliate_id: str
    name: str