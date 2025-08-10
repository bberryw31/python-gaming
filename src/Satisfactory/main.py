import json
from dataclasses import dataclass
from collections import defaultdict


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


class SatisfactoryOptimizer:
    def __init__(self, data_path='data.json'):
        """Initialize optimizer with game data"""
        # Define early-mid game items (up to Space Elevator Phase 3)
        self.early_game_items = {
            # Basic materials
            'iron-ore', 'copper-ore', 'limestone', 'coal',
            'caterium-ore', 'raw-quartz', 'sulfur', 'crude-oil',
            # ... rest of items
        }

        try:
            with open(data_path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"recipes": [], "buildings": [], "resources": [], "miners": [], "items": [], "fluids": []}

        self.recipes = self._parse_recipes()
        self.buildings = self._parse_buildings()
        self.resources = self._parse_resources()
        self.miners = self._parse_miners()
        self.items = {item['key_name']: item['name'] for item in self.data.get('items', [])}
        self.fluids = {fluid['key_name']: fluid['name'] for fluid in self.data.get('fluids', [])}

        # Combine items and fluids for display
        self.all_items = {**self.items, **self.fluids}

    def _parse_recipes(self):
        """Parse recipes from JSON data, only using primary recipes up to mid-game"""
        # Implementation here

    def _parse_buildings(self):
        """Parse building data"""
        return {b['category']: b for b in self.data.get('buildings', [])}

    def _parse_resources(self):
        """Parse resource data"""
        return {r['key_name']: r for r in self.data.get('resources', [])}

    def _parse_miners(self):
        """Parse miner data"""
        return {m['key_name']: m for m in self.data.get('miners', [])}