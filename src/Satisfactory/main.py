import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
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

            # Basic processed
            'iron-ingot', 'copper-ingot', 'steel-ingot', 'caterium-ingot',
            'concrete', 'quartz-crystal', 'silica',

            # Basic parts
            'iron-plate', 'iron-rod', 'screw', 'wire', 'cable', 'quickwire',
            'copper-sheet', 'steel-beam', 'steel-pipe',

            # Intermediate parts
            'reinforced-iron-plate', 'modular-frame', 'rotor', 'stator',
            'motor', 'encased-industrial-beam',

            # Oil products (Tier 5)
            'plastic', 'rubber', 'fuel', 'petroleum-coke', 'polymer-resin',
            'heavy-oil-residue',

            # Electronics (up to Tier 5-6)
            'circuit-board', 'computer', 'high-speed-connector', 'ai-limiter',

            # Advanced but still mid-game
            'heavy-modular-frame', 'crystal-oscillator', 'black-powder',

            # Space Elevator items for Phase 1-3
            'smart-plating', 'versatile-framework', 'automated-wiring',
            'modular-engine', 'adaptive-control-unit'
        }

        try:
            with open(data_path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Data file '{data_path}' not found!")
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
        recipes_by_product = {}

        for recipe_data in self.data.get('recipes', []):
            # Skip alternate recipes
            if 'alt-' in recipe_data.get('key_name', ''):
                continue

            # Skip converter, nuclear, and advanced recipes
            if recipe_data.get('category', '') in ['converting', 'nuke-reacting', 'accelerating', 'encoding']:
                continue

            ingredients = {ing[0]: ing[1] for ing in recipe_data.get('ingredients', [])}
            products = {prod[0]: prod[1] for prod in recipe_data.get('products', [])}

            # Skip recipes with late-game materials
            skip_materials = {
                'reanimated-sam', 'sam', 'uranium', 'plutonium-pellet',
                'uranium-waste', 'bauxite', 'aluminum-scrap', 'aluminum-ingot',
                'battery', 'supercomputer', 'alumina-solution', 'sulfuric-acid',
                'nitrogen-gas', 'nitric-acid', 'turbofuel', 'aluminum-casing',
                'alclad-aluminum-sheet', 'radio-control-unit', 'turbo-motor'
            }

            if any(mat in ingredients for mat in skip_materials):
                continue
            if any(mat in products for mat in skip_materials):
                continue

            # Only include recipes where all products are in early game set
            if not all(prod in self.early_game_items for prod in products):
                continue

            recipe = Recipe(
                name=recipe_data['name'],
                key_name=recipe_data['key_name'],
                category=recipe_data['category'],
                time=recipe_data['time'],
                ingredients=ingredients,
                products=products
            )

            # Store by main product
            for product in products:
                if product not in recipes_by_product:
                    recipes_by_product[product] = recipe
                    break

        return recipes_by_product

    def _parse_buildings(self):
        """Parse building data"""
        return {b['category']: b for b in self.data.get('buildings', [])}

    def _parse_resources(self):
        """Parse resource data"""
        return {r['key_name']: r for r in self.data.get('resources', [])}

    def _parse_miners(self):
        """Parse miner data"""
        return {m['key_name']: m for m in self.data.get('miners', [])}

    def calculate_production_chain(self, target_item, available_resources=None):
        """Calculate the production chain for a target item with natural production rates"""
        # Get the base recipe for the target item
        if target_item not in self.recipes:
            return {
                'target': target_item,
                'target_rate': 0,
                'recipes_used': {},
                'buildings_needed': defaultdict(float),
                'raw_materials': defaultdict(float),
                'power_consumption': 0,
                'warnings': [f"No recipe found for {target_item}"],
                'production_tree': None
            }

        # Get the natural output rate of one building
        base_recipe = self.recipes[target_item]
        base_output_rate = base_recipe.get_items_per_minute().get(target_item, 0)

        chain = {
            'target': target_item,
            'target_rate': base_output_rate,
            'recipes_used': {},
            'buildings_needed': defaultdict(float),
            'raw_materials': defaultdict(float),
            'power_consumption': 0,
            'warnings': [],
            'production_tree': None
        }

        # Track items being processed to detect cycles
        processing_stack = set()

        def build_production_tree(item, rate, depth=0, path=None):
            # Tree building logic here
            pass

        # Build the production tree starting with natural output rate
        chain['production_tree'] = build_production_tree(target_item, base_output_rate)

        # Calculate resource node requirements if provided
        if available_resources:
            chain['resource_nodes_needed'] = self._calculate_resource_nodes(
                chain['raw_materials'], available_resources)

        return chain

    def _calculate_resource_nodes(self, raw_materials, available_resources):
        """Calculate resource node utilization"""
        nodes_needed = {}

        # Group available resources by type
        resources_by_type = defaultdict(list)
        for res in available_resources:
            resources_by_type[res.resource_type].append(res)

        for material, rate_needed in raw_materials.items():
            available_nodes = resources_by_type.get(material, [])

            if not available_nodes:
                nodes_needed[material] = {
                    'required_rate': rate_needed,
                    'available_rate': 0,
                    'shortage': rate_needed,
                    'utilization': 0
                }
                continue

            # Calculate total available rate
            total_available = 0
            for node in available_nodes:
                resource_data = self.resources.get(material, {})
                category = resource_data.get('category', 'mineral')

                if category == 'mineral':
                    miner_key = f"miner-mk{node.miner_mk}"
                elif category == 'oil':
                    miner_key = 'oil-pump'
                else:
                    miner_key = f"miner-mk{node.miner_mk}"

                miner = self.miners.get(miner_key, {})
                base_rate = miner.get('base_rate', 60)
                node_rate = node.get_output_rate(base_rate)
                total_available += node_rate

            nodes_needed[material] = {
                'required_rate': rate_needed,
                'available_rate': total_available,
                'shortage': max(0, rate_needed - total_available),
                'utilization': min(100, (rate_needed / total_available * 100)) if total_available > 0 else 0
            }

        return nodes_needed