import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Windows
import matplotlib.pyplot as plt
import pathlib
from typing import List, Dict
import numpy as np

class Roofline:
    def __init__(self):
        self.arith_unit = "FLOPS"
        self.data_unit = "bytes"
        self.max_arith = None
        self.max_bandwidth = None
        self.points: List[Dict] = []
        self.category_colors = {}  # Stores custom color mappings
        self._color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        
    def set_units(self, arith_unit: str, data_unit: str) -> None:
        """Set units for arithmetic intensity and performance"""
        self.arith_unit = arith_unit
        self.data_unit = data_unit
        
    def set_ideal(self, max_arith: float, max_bandwidth: float) -> None:
        """Set the performance ceilings for ideal roofline"""
        if max_arith <= 0 or max_bandwidth <= 0:
            raise ValueError("Performance values must be positive")
        self.max_arith = max_arith
        self.max_bandwidth = max_bandwidth
        
    def set_palette(self, palette: dict) -> None:
        """Set color palette for categories"""
        if not isinstance(palette, dict):
            raise TypeError("Palette must be a dictionary")
        self.category_colors.update(palette)

    def add_point(self, throughput: float, intensity: float, category: str) -> None:
        """Add a data point with category for coloring"""
        if throughput <= 0 or intensity <= 0:
            raise ValueError("Throughput and data amount must be positive")
            
        self.points.append({
            'throughput': throughput,
            'intensity': intensity,
            'category': category
        })
        
    def plot(self, figure_path: pathlib.Path) -> None:
        """Generate and save the roofline plot"""
        try:
            if not self.max_arith or not self.max_bandwidth:
                raise RuntimeError("Must set ideal performance with set_ideal() before plotting")
            
            plt.figure(figsize=(8, 6))
            ax = plt.gca()

            # Calculate arithmetic intensity for all points
            intensities = [p['intensity'] for p in self.points]
            performances = [p['throughput'] for p in self.points]
            
            # Plot roofline
            ai = np.linspace(0, (max(intensities) if intensities else 1), 100)
            roof = np.minimum(self.max_arith, self.max_bandwidth * ai)
            plt.plot(ai, roof, 'k--', label='Roofline')
            
            # Plot points with category colors
            categories = {p['category'] for p in self.points}
            for i, category in enumerate(categories):
                cat_points = [p for p in self.points if p['category'] == category]
                c = self.category_colors.get(category, self._color_cycle[i % len(self._color_cycle)])
                x = [p['intensity'] for p in cat_points]
                y = [p['throughput'] for p in cat_points]
                plt.scatter(x, y, color=c, label=category, zorder=10)

            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel(f"Arithmetic Intensity ({self.arith_unit}/{self.data_unit})")
            plt.ylabel(f"Performance ({self.arith_unit})")
            plt.title("Roofline Model")
            plt.legend()
            plt.grid(True, which='both', linestyle='--')
            plt.tight_layout()
            figure_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(figure_path, format='pdf', bbox_inches='tight')
            plt.close()
            print(f"Successfully saved plot to {figure_path.absolute()}")
        except Exception as e:
            print(f"Error generating plot: {str(e)}")
            raise
