# Roofline Model Visualization Package

A Python class for generating roofline model plots with customizable data points and performance ceilings, mainly written by DeepSeek-r1

## Installation

```bash
pip install roofline-plotter
```

## Basic Usage

```python
import pathlib
from roofline import Roofline

# Initialize plotter
rl = Roofline()

# Configure units and performance limits
rl.set_units("FLOPS", "bytes")
rl.set_ideal(max_arith=100, max_bandwidth=50)  # Your hardware limits

# Add data points
rl.add_point(80, 2, category="Kernel A")
rl.add_point(45, 1.5, category="Kernel B")

# Generate plot
rl.plot(pathlib.Path("roofline_plot.pdf"))
```

## Customization

### Category Colors
```python
rl.set_palette({
    "Kernel A": "#FF5733",
    "Kernel B": "#33FF57",
    "Optimized": "#3357FF"
})
```

## API Reference

### `Roofline` Class Methods

- **set_units(arith_unit: str, data_unit: str)**  
  Set measurement units for axes labels

- **set_ideal(max_arith: float, max_bandwidth: float)**  
  Define performance ceilings (arithmetic intensity vs bandwidth)

- **add_point(throughput: float, data_amount: float, category: str)**  
  Add a benchmark result with classification

- **set_palette(palette: dict)**  
  Customize category colors {category_name: hex_color}

- **plot(figure_path: pathlib.Path)**  
  Generate and save PDF plot with current configuration
