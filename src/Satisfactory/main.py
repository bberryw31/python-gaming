import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pandas as pd
from dataclasses import dataclass
from collections import defaultdict
import math


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
            'target_rate': base_output_rate,  # Natural rate from one building
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
            """Build tree structure while calculating requirements"""
            if path is None:
                path = []

            node = {
                'item': item,
                'display_name': self.all_items.get(item, item),
                'rate': rate,
                'depth': depth,
                'children': [],
                'recipe': None,
                'buildings': 0,
                'is_raw': False
            }

            # Check for cycles
            if item in processing_stack:
                node['is_cycle'] = True
                chain['warnings'].append(f"Circular dependency: {' -> '.join(path + [item])}")
                chain['raw_materials'][item] += rate
                return node

            # Check if this is a raw material
            if item not in self.recipes:
                chain['raw_materials'][item] += rate
                node['is_raw'] = True
                return node

            # Get recipe for this item
            recipe = self.recipes[item]
            node['recipe'] = recipe.name

            # Calculate buildings needed
            items_per_min = recipe.get_items_per_minute()
            output_rate = items_per_min.get(item, 0)

            if output_rate == 0:
                chain['warnings'].append(f"Recipe {recipe.name} doesn't produce {item}")
                chain['raw_materials'][item] += rate
                node['is_raw'] = True
                return node

            num_buildings = rate / output_rate
            node['buildings'] = num_buildings

            # Track recipe usage
            recipe_key = recipe.name
            if recipe_key not in chain['recipes_used']:
                chain['recipes_used'][recipe_key] = {
                    'recipe': recipe.name,
                    'buildings': 0,
                    'inputs_per_min': recipe.get_inputs_per_minute(),
                    'outputs_per_min': items_per_min,
                    'depth': depth
                }
            chain['recipes_used'][recipe_key]['buildings'] += num_buildings

            # Track building usage
            building = self.buildings.get(recipe.category, {})
            building_name = building.get('name', recipe.category)
            chain['buildings_needed'][building_name] += num_buildings

            # Calculate power consumption
            base_power = building.get('power', 0)
            chain['power_consumption'] += base_power * num_buildings

            # Process ingredients recursively
            processing_stack.add(item)
            inputs_per_min = recipe.get_inputs_per_minute()
            for ingredient, amount in inputs_per_min.items():
                required_rate = amount * num_buildings
                child_node = build_production_tree(ingredient, required_rate, depth + 1, path + [item])
                node['children'].append(child_node)
            processing_stack.remove(item)

            return node

        # Build the production tree starting with natural output rate
        chain['production_tree'] = build_production_tree(target_item, base_output_rate)

        # Calculate resource node requirements if provided
        if available_resources:
            chain['resource_nodes_needed'] = self._calculate_resource_nodes(
                chain['raw_materials'], available_resources
            )

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


class SatisfactoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Satisfactory Factory Optimizer")
        self.root.geometry("1400x900")

        # Initialize optimizer
        self.optimizer = SatisfactoryOptimizer('data.json')

        # Store resource nodes
        self.resource_nodes = []

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        """Create all GUI widgets"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Main calculation tab
        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text='Production Calculator')
        self.create_main_tab(main_tab)

        # Tree visualization tab
        tree_tab = ttk.Frame(notebook)
        notebook.add(tree_tab, text='Production Tree')
        self.create_tree_tab(tree_tab)

    def create_main_tab(self, parent):
        """Create the main calculation interface"""
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill='both', expand=True)

        # Resource Configuration Frame
        resource_frame = ttk.LabelFrame(main_frame, text="Resource Nodes Configuration", padding="10")
        resource_frame.pack(fill='x', pady=5)

        controls_frame = ttk.Frame(resource_frame)
        controls_frame.pack(fill='x')

        # Resource type dropdown - only early game resources
        ttk.Label(controls_frame, text="Resource Type:").grid(row=0, column=0, padx=5)
        self.resource_type_var = tk.StringVar()

        # Only include resources available in early-mid game (no crude oil or water)
        resource_types = ['iron-ore', 'copper-ore', 'limestone', 'coal',
                          'caterium-ore', 'raw-quartz', 'sulfur']

        self.resource_combo = ttk.Combobox(controls_frame, textvariable=self.resource_type_var,
                                           values=resource_types, width=20)
        self.resource_combo.grid(row=0, column=1, padx=5)
        self.resource_combo.set('iron-ore')

        # Purity dropdown
        ttk.Label(controls_frame, text="Purity:").grid(row=0, column=2, padx=5)
        self.purity_var = tk.StringVar()
        self.purity_combo = ttk.Combobox(controls_frame, textvariable=self.purity_var,
                                         values=['impure', 'normal', 'pure'], width=10)
        self.purity_combo.grid(row=0, column=3, padx=5)
        self.purity_combo.set('normal')

        # Miner Mk dropdown
        ttk.Label(controls_frame, text="Miner:").grid(row=0, column=4, padx=5)
        self.miner_var = tk.StringVar()
        self.miner_combo = ttk.Combobox(controls_frame, textvariable=self.miner_var,
                                        values=['Mk1', 'Mk2', 'Mk3'], width=10)
        self.miner_combo.grid(row=0, column=5, padx=5)
        self.miner_combo.set('Mk1')  # Default to Mk1

        # Buttons
        ttk.Button(controls_frame, text="Add Resource",
                   command=self.add_resource).grid(row=0, column=6, padx=5)
        ttk.Button(controls_frame, text="Clear All",
                   command=self.clear_resources).grid(row=0, column=7, padx=5)

        # Resource list
        self.resource_listbox = tk.Listbox(resource_frame, height=5)
        self.resource_listbox.pack(fill='x', pady=5)

        # Target Configuration Frame
        target_frame = ttk.LabelFrame(main_frame, text="Production Target", padding="10")
        target_frame.pack(fill='x', pady=5)

        # Target item dropdown
        ttk.Label(target_frame, text="Target Item:").pack(side='left', padx=5)
        self.target_var = tk.StringVar()

        # Get all producible items
        producible_items = sorted([
            self.optimizer.all_items.get(item, item)
            for item in self.optimizer.recipes.keys()
        ])

        self.target_combo = ttk.Combobox(target_frame, textvariable=self.target_var,
                                         values=producible_items, width=40)
        self.target_combo.pack(side='left', padx=5)
        if producible_items:
            self.target_combo.set(producible_items[0])

        # Calculate button
        ttk.Button(target_frame, text="Calculate Production Chain",
                   command=self.calculate_chain).pack(side='left', padx=20)

        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Production Chain Results", padding="10")
        results_frame.pack(fill='both', expand=True, pady=5)

        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=25)
        self.results_text.pack(fill='both', expand=True)

    def create_tree_tab(self, parent):
        """Create the tree visualization tab"""
        tree_frame = ttk.Frame(parent, padding="10")
        tree_frame.pack(fill='both', expand=True)

        # Info label
        info_label = ttk.Label(tree_frame,
                               text="Calculate a production chain first, then view the tree structure here")
        info_label.pack(pady=5)

        # Tree text area with monospace font
        self.tree_text = scrolledtext.ScrolledText(tree_frame, wrap=tk.NONE,
                                                   font=('Courier', 10))
        self.tree_text.pack(fill='both', expand=True)

    def add_resource(self):
        """Add a resource node to the list"""
        resource_type = self.resource_type_var.get()
        purity = self.purity_var.get()
        miner = self.miner_var.get()

        if resource_type and purity and miner:
            miner_mk = int(miner[-1])
            node = ResourceNode(resource_type, purity, miner_mk)
            self.resource_nodes.append(node)

            display_text = f"{resource_type} - {purity} - {miner}"
            self.resource_listbox.insert(tk.END, display_text)

    def clear_resources(self):
        """Clear all resource nodes"""
        self.resource_nodes = []
        self.resource_listbox.delete(0, tk.END)

    def calculate_chain(self):
        """Calculate the production chain"""
        # Get target item key from display name
        target_display = self.target_var.get()
        target_key = None
        for key, name in self.optimizer.all_items.items():
            if name == target_display:
                target_key = key
                break

        if not target_key:
            messagebox.showerror("Error", "Please select a valid target item")
            return

        # Calculate production chain (always at 1 item/min)
        chain = self.optimizer.calculate_production_chain(
            target_item=target_key,
            available_resources=self.resource_nodes
        )

        # Display results
        self.display_results(chain)
        self.display_tree(chain['production_tree'])

        # Store chain for export
        self.current_chain = chain

    def display_tree(self, tree_node, indent="", is_last=True, prefix=""):
        """Display the production tree in a visual format"""
        if tree_node is None:
            return

        # Clear tree text on first call
        if indent == "":
            self.tree_text.delete(1.0, tk.END)
            self.tree_text.insert(tk.END, "PRODUCTION TREE VISUALIZATION\n")
            self.tree_text.insert(tk.END, "=" * 60 + "\n\n")

        # Create tree branch characters
        if indent == "":
            branch = ""
        elif is_last:
            branch = "└── "
        else:
            branch = "├── "

        # Format node information
        node_info = f"{tree_node['display_name']} ({tree_node['rate']:.2f}/min)"

        if tree_node.get('is_raw'):
            node_info += " [RAW MATERIAL]"
        elif tree_node.get('is_cycle'):
            node_info += " [CIRCULAR DEPENDENCY]"
        elif tree_node.get('recipe'):
            node_info += f" via {tree_node['recipe']}"
            if tree_node['buildings'] > 0:
                node_info += f" x{tree_node['buildings']:.2f} buildings"

        # Insert the node
        self.tree_text.insert(tk.END, prefix + branch + node_info + "\n")

        # Process children
        if tree_node.get('children'):
            if indent == "":
                new_prefix = ""
            elif is_last:
                new_prefix = prefix + "    "
            else:
                new_prefix = prefix + "│   "

            for i, child in enumerate(tree_node['children']):
                is_last_child = (i == len(tree_node['children']) - 1)
                self.display_tree(child, indent + "    ", is_last_child, new_prefix)

    def display_results(self, chain):
        """Display production chain results"""
        self.results_text.delete(1.0, tk.END)

        # Header
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, f"PRODUCTION CHAIN FOR: {chain['target']}\n")
        self.results_text.insert(tk.END, f"Output: {chain['target_rate']:.2f}/min from 1 building\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")

        # Summary
        self.results_text.insert(tk.END, "📊 SUMMARY:\n")
        total_buildings = sum(math.ceil(count) for count in chain['buildings_needed'].values())
        self.results_text.insert(tk.END, f"  • Total Buildings: {total_buildings}\n")
        self.results_text.insert(tk.END, f"  • Power Consumption: {chain['power_consumption']:.1f} MW\n")
        self.results_text.insert(tk.END, f"  • Different Recipes: {len(chain['recipes_used'])}\n\n")

        # Recipes used
        self.results_text.insert(tk.END, "📦 RECIPES USED:\n")
        for recipe_key, info in sorted(chain['recipes_used'].items(), key=lambda x: x[1]['depth']):
            indent = "  " * (info['depth'] + 1)
            self.results_text.insert(tk.END,
                                     f"{indent}• {info['recipe']}: {info['buildings']:.2f} buildings\n")

            inputs = ', '.join([f'{v:.2f} {self.optimizer.all_items.get(k, k)}/min'
                                for k, v in info['inputs_per_min'].items()])
            outputs = ', '.join([f'{v:.2f} {self.optimizer.all_items.get(k, k)}/min'
                                 for k, v in info['outputs_per_min'].items()])
            self.results_text.insert(tk.END, f"{indent}  Inputs: {inputs}\n")
            self.results_text.insert(tk.END, f"{indent}  Outputs: {outputs}\n")

        # Buildings needed
        self.results_text.insert(tk.END, "\n🏭 BUILDINGS NEEDED:\n")
        for building, count in sorted(chain['buildings_needed'].items()):
            self.results_text.insert(tk.END, f"  • {building}: {math.ceil(count)} ({count:.2f})\n")

        # Raw materials
        self.results_text.insert(tk.END, "\n⛏️ RAW MATERIALS:\n")
        for material, rate in sorted(chain['raw_materials'].items()):
            material_name = self.optimizer.all_items.get(material, material)
            self.results_text.insert(tk.END, f"  • {material_name}: {rate:.2f}/min\n")

        # Resource nodes analysis
        if 'resource_nodes_needed' in chain:
            self.results_text.insert(tk.END, "\n🗺️ RESOURCE NODES ANALYSIS:\n")
            for material, info in chain['resource_nodes_needed'].items():
                material_name = self.optimizer.all_items.get(material, material)
                status = "✅" if info['shortage'] == 0 else "⚠️"
                self.results_text.insert(tk.END,
                                         f"  {status} {material_name}: {info['required_rate']:.2f}/min "
                                         f"(Available: {info['available_rate']:.1f}/min, "
                                         f"Utilization: {info['utilization']:.1f}%)\n")
                if info['shortage'] > 0:
                    self.results_text.insert(tk.END,
                                             f"      ⚠️ SHORTAGE: {info['shortage']:.2f}/min\n")

        # Warnings
        if chain['warnings']:
            self.results_text.insert(tk.END, "\n⚠️ WARNINGS:\n")
            for warning in chain['warnings']:
                self.results_text.insert(tk.END, f"  • {warning}\n")

    def export_results(self):
        """Export results to CSV file"""
        if not hasattr(self, 'current_chain'):
            messagebox.showwarning("Warning", "No results to export. Please calculate first.")
            return

        # Create DataFrame
        data = []
        for recipe_key, info in self.current_chain['recipes_used'].items():
            data.append({
                'Recipe': info['recipe'],
                'Buildings_Exact': f"{info['buildings']:.2f}",
                'Buildings_Needed': math.ceil(info['buildings']),
                'Inputs/min': ', '.join([f"{v:.2f} {k}" for k, v in info['inputs_per_min'].items()]),
                'Outputs/min': ', '.join([f"{v:.2f} {k}" for k, v in info['outputs_per_min'].items()])
            })

        df = pd.DataFrame(data)

        # Save to CSV
        filename = f"satisfactory_chain_{self.current_chain['target']}.csv"
        df.to_csv(filename, index=False)
        messagebox.showinfo("Success", f"Results exported to {filename}")


def main():
    root = tk.Tk()
    app = SatisfactoryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()