import json
from dataclasses import dataclass


@dataclass
class ResourceNode:
    """Represents a resource node with purity and miner configuration"""
    resource_type: str
    purity: str
    miner_mk: int

    def get_purity_multiplier(self):
        multipliers = {'impure': 0.5, 'normal': 1.0, 'pure': 2.0}
        return multipliers.get(self.purity, 1.0)

    def get_output_rate(self, base_rate):
        """Calculate actual output rate based on purity and miner"""
        return base_rate * self.get_purity_multiplier()


@dataclass
class Recipe:
    """Represents a crafting recipe"""
    name: str
    key_name: str
    category: str
    time: float
    ingredients: dict
    products: dict

    def get_items_per_minute(self):
        """Calculate items per minute for products"""
        return {item: (amount * 60 / self.time) for item, amount in self.products.items()}

    def get_inputs_per_minute(self):
        """Calculate items per minute for inputs"""
        return {item: (amount * 60 / self.time) for item, amount in self.ingredients.items()}