<p align="center">
   <img width="200" height="200" alt="FoamifyLogo" src="https://github.com/user-attachments/assets/a83da7fe-3259-4b1a-a97c-4a715a7d9d53" />
</p>

**Welcome to Foamify** — an interactive, randomized foam generator designed for scientific modeling and visualization. Foamify creates coordinate files specifying the locations and radii of a randomly generated ensemble of spheres, allowing users to produce custom foams for a wide range of applications. These virtual foams can be used to simulate and analyze physics-based systems such as aerated media, porous materials, and other complex microstructures. Sphere generation is governed by a flexible set of user-defined parameters (see [Parameters](Parameters), offering full control over the statistical and geometric characteristics of the output.

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

Foamify outputs simple coordinate and radius data in plain-text format, compatible with visualization and analysis tools. This includes native support for PyMOL, as well as seamless interoperability with Vorpy, a Voronoi-based geometry analysis tool developed in the same lab.

The project was created in collaboration with the Chemistry Department at Georgia State University and is published on PyPI for easy installation and use within existing Python codebases. For usage examples and API documentation, see the [Usage](Usage) section. 

# Features

- **3D Sphere Generation**: Create random ensembles of spheres in 3D space
- **Customizable Parameters**: Adjust size, distribution, and interaction of spheres
- **Interactive GUI**: User-friendly graphical interface for parameter configuration
- **Export Capabilities**: Save generated foam structures for further analysis
- **Visualization Tools**: Built-in plotting and visualization features
- **Machine Learning Integration**: Advanced density adjustment algorithms

# Installation

## From PyPI (Recommended)

```bash
pip install foamify
```

## From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/jackericson98/foamify.git
   cd foamify
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

<a name="Usage"></a>
# Usage

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

   
