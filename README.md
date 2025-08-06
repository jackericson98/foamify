<p align="center">
   <img width="200" height="200" alt="FoamifyLogo" src="https://github.com/user-attachments/assets/a83da7fe-3259-4b1a-a97c-4a715a7d9d53" />
</p>

Welcome to Foamify, an interactive 3D randomized foam generator! Foamify generates the locations and radii of a random ensemble of 3D spheres that fall within a range of parameters. The spheres can be used to mimic bubbles in a foam allowing the user to perform complex analysis on simulated physics-based materials. 

# Overview

Foamify was developed in python and has been turned into a python package of its own. This allows for easy integration into the users existing code base (see [Usage](Usage). 

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

   
