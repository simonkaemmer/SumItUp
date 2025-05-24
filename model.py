from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Item:
    name: str
    categorie: str
    cost: Decimal

    def get_as_entry(self) -> list:
        return {'name': self.name, 'cat': self.categorie, 'cost': self.cost}

