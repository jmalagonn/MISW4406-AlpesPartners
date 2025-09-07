from dataclasses import dataclass

@dataclass
class CreateAffiliate:
    name: str
    created_at: str

@dataclass
class RenameAffiliate:
    id: str
    name: str