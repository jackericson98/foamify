<p align="center">
   <img width="200" height="200" alt="FoamifyLogo" src="https://github.com/user-attachments/assets/a83da7fe-3259-4b1a-a97c-4a715a7d9d53" />
</p>

**Welcome to Foamify** — an interactive, randomized foam generator designed for scientific modeling and visualization. Foamify creates coordinate files specifying the locations and radii of a randomly generated ensemble of spheres, allowing users to produce custom foams for a wide range of applications. These virtual foams can be used to simulate and analyze physics-based systems such as aerated media, porous materials, and other complex microstructures. Sphere generation is governed by a flexible set of user-defined parameters (see [Parameters](#Parameters), offering full control over the statistical and geometric characteristics of the output.

# Overview

Foamify is a lightweight and flexible Python package for generating randomized sphere ensembles with tunable geometric properties. It was developed to support modeling of disordered systems such as foams, aerated media, and porous materials, and is suited for integration into simulation pipelines or exploratory analysis tools.

The generator provides control over key structural parameters, including:

- Density
- Mean radius
- Polydispersity
- Number of spheres
- Overlap percentage
- Distribution type
- Periodicity

Foamify outputs simple coordinate and radius data in plain-text format, compatible with visualization and analysis tools. This includes native support for (PyMOL)[pymol.org], as well as seamless interoperability with [VorPy](https://github.com/jackericson98/vorpy), a Voronoi-based geometry analysis tool developed in the same lab.

The project was created in collaboration with the Chemistry Department at Georgia State University and is published on PyPI for easy installation and use within existing Python codebases. For usage examples and API documentation, see the [Usage](#Usage) section. 

# Features

- **Randomized 3D Sphere Generation**
   Generate disordered sphere packings in three-dimensional space to represent open- or closed-celled foams. Each run creates a unique configuration based on randomized seeds, with full reproducibility via seed locking.

- **Customizable Geometry Parameters**
   Control key physical and geometric features of the output foam, including total number of spheres, mean radius, density, polydispersity, overlap percentage, and distribution type (e.g., uniform, normal). Supports both bounded and periodic systems.

- **Interactive GUI (Optional)**
   A lightweight, optional graphical interface is included for real-time parameter tuning and instant feedback on generated foams. Useful for prototyping and educational purposes.

- **Command-Line and Programmatic Interfaces**
   Foamify can be used directly from the command line or imported as a Python module. Designed for flexibility in scripting, integration, or batch-processing workflows.

- **PyPI Integration**
   Foamify is fully packaged and published on the Python Package Index (PyPI), allowing for simple installation via pip install foamify. This makes integration into existing codebases fast and dependency management easy.

- **Exportable Output Files**
   Outputs are saved in standard, human-readable coordinate files that include each sphere’s center and radius. These files can be directly used with visualization tools or passed to downstream simulation software.

- **Visualization Support**
   Includes optional built-in plotting functions (e.g., 2D cross-sections, histograms of radius distributions), and exports are compatible with PyMOL and other 3D viewers for structural inspection.

- **Compatible with Vorpy Analysis Suite**
   Foamify outputs are directly compatible with Vorpy, enabling Voronoi-based spatial partitioning and curvature analysis. This supports advanced geometric characterization of the generated structures.

- **Machine Learning–Enhanced Algorithms (Experimental)**
   Includes preliminary integration of machine learning algorithms for smart density tuning and optimized foam construction. These methods aim to balance randomness with physical plausibility.

- **Modular and Lightweight Codebase**
   Designed with modular architecture and minimal external dependencies. Easy to extend or modify for specific research applications.

<a name="Usage"></a>
# Usage

## Installation

### From PyPI (Recommended)

```bash
pip install foamify
```

### From Source

```bash
git clone https://github.com/jackericson98/foamify.git
cd foamify
```

The general workflow for Foamify is as follows:

1. **Launch the GUI**: Run `foamify`
2. **Configure Parameters**: Set your desired foam parameters through the interface
3. **Generate Foam**: Click "Create Foam" to generate your 3D sphere ensemble
4. **Export Results**: Save your generated foam for further analysis

<a name="Parameters"></a>
# Parameters

The foam generation can be customized with various parameters including:
- Sphere size distributions
- Density settings
- Spatial arrangement
- Interaction parameters

# Dependencies

- Python >= 3.8
- numpy >= 1.21.0
- scipy >= 1.7.0
- matplotlib >= 3.5.0
- numba >= 0.56.0
- pandas >= 1.3.0
- scikit-learn >= 1.0.0
- tqdm >= 4.62.0

# Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Author

**John Ericson** - Georgia State University (2025)

- Email: jackericson98@gmail.com
- GitHub: [@jackericson98](https://github.com/jackericson98)
- Website: [ericsonlabs.com](https://www.ericsonlabs.com)
- LinkedIn: 

# Citation

Foamify is open-source for a reason! We would love for you to use our software and even request features, but we also would you to toss us a bone if you do. If you use this software in your research, please cite:

```bibtex
@software{foamify,
  title={foamify: Interactive 3D Foam Generator},
  author={John Ericson},
  year={2025},
  url={https://github.com/jackericson98/foamify}
}
```

# Support

- **Issues**: [GitHub Issues](https://github.com/jackericson98/foamify/issues)
- **Documentation**: [GitHub README](https://github.com/jackericson98/foamify#readme)

   
