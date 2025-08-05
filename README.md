# foamify

An interactive simulated foam generator for creating 3-dimensional random ensembles of spheres.

## Overview

`foamify` is a Python package designed to create 3-dimensional random ensembles of spheres, mimicking the bubbles in foam based on user-defined parameters. This tool is particularly useful for researchers and scientists working in materials science, physics, and engineering applications.

## Features

- **3D Sphere Generation**: Create random ensembles of spheres in 3D space
- **Customizable Parameters**: Adjust size, distribution, and interaction of spheres
- **Interactive GUI**: User-friendly graphical interface for parameter configuration
- **Export Capabilities**: Save generated foam structures for further analysis
- **Visualization Tools**: Built-in plotting and visualization features
- **Machine Learning Integration**: Advanced density adjustment algorithms

## Installation

### From PyPI (Recommended)

```bash
pip install foamify
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/jackericson98/foamify.git
   cd foamify
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

## Quick Start

### Command Line Interface

After installation, run the interactive GUI:

```bash
foamify
```

Or run as a Python module:

```bash
python -m foam_gen
```

### Python API

```python
import foam_gen

# Use the package programmatically
# (API documentation coming soon)
```

## Usage

1. **Launch the GUI**: Run `foamify` from your terminal
2. **Configure Parameters**: Set your desired foam parameters through the interface
3. **Generate Foam**: Click "Create Foam" to generate your 3D sphere ensemble
4. **Export Results**: Save your generated foam for further analysis

## Parameters

The foam generation can be customized with various parameters including:
- Sphere size distributions
- Density settings
- Spatial arrangement
- Interaction parameters

## Dependencies

- Python >= 3.8
- numpy >= 1.21.0
- scipy >= 1.7.0
- matplotlib >= 3.5.0
- numba >= 0.56.0
- pandas >= 1.3.0
- scikit-learn >= 1.0.0
- tqdm >= 4.62.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**John Ericson** - Georgia State University (2025)

- Email: jackericson98@gmail.com
- GitHub: [@jackericson98](https://github.com/jackericson98)

## Citation

If you use this software in your research, please cite:

```bibtex
@software{foamify,
  title={foamify: Interactive 3D Foam Generator},
  author={John Ericson},
  year={2025},
  url={https://github.com/jackericson98/foamify}
}
```

## Support

- **Issues**: [GitHub Issues](https://github.com/jackericson98/foamify/issues)
- **Documentation**: [GitHub README](https://github.com/jackericson98/foamify#readme)

   
