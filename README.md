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

<a name="Parameters"></a>

# Parameters

Foamify supports a range of customizable parameters that define the geometric and statistical properties of the generated foam. These inputs allow you to tailor the output to specific physical or simulation constraints.

### 📏 **Size & Distribution Parameters**

- **`Mean Radius`** *(float, default: 1.0)*  
  Average radius of the spheres. Controls the general scale of the structure.  
  **Typical range**: `0.1 – 1000.0`

- **`Polydispersity`** *(float, default: 0.25)*  
  Controls the spread of the sphere sizes. A value of 0 produces monodisperse spheres; higher values introduce variability. Corresponds to the coefficient of variation of the distribution of radii. 
  **Typical range**: `0.0 – 10.0`

- **`Distribution Type`** *(str, default: `'normal'`)*  
  Statistical distribution used to generate sphere radii.  
  **Options**:
  - `'uniform'` – all sizes within a fixed range  
  - `'normal'` – bell curve centered on mean  
  - `'lognormal'` – skewed distributions for highly porous media

### 📦 **Spatial Parameters**

- **`num_spheres`** *(int, default: 1000)*  
  Total number of spheres to be generated in the foam. Affects computational cost and packing density.  
  **Typical range**: `10 – 100,000+`

- **`box_size`** *(float or 3-tuple, default: auto)*  
  Size of the bounding volume (either cubic or rectangular). If set to `auto`, the box will be scaled based on target density and number of spheres.  
  **Typical range**: `5.0 – 500.0`

- **`density`** *(float, default: 0.2)*  
  Target packing density of the foam. Defines the volume fraction of the space occupied by spheres.  
  **Typical range**: `0.01 – 0.74`  
  *(0.74 = maximum for ordered packings like FCC)*

- **`periodic`** *(bool, default: False)*  
  Whether to apply periodic boundary conditions. When `True`, spheres near the boundaries wrap around, allowing tiling and simulation of infinite domains.

### ⚙️ **Interaction & Placement Parameters**

- **`overlap_percentage`** *(float, default: 0.0)*  
  Maximum allowable overlap between neighboring spheres, as a percentage of the smaller radius. Set to zero for non-overlapping packings.  
  **Typical range**: `0.0 – 0.3`

- **`min_distance`** *(float, optional)*  
  Minimum center-to-center distance allowed between spheres. Overrides overlap percentage if set.

- **`seed`** *(int, optional)*  
  Random seed for reproducible output. Use the same seed to regenerate identical foam configurations.

### 🧪 **Advanced / Experimental Parameters**

- **`bias_centering`** *(bool, default: False)*  
  Whether to bias sphere placement toward the center of the domain. Useful for simulating structures with graded density.

- **`fixed_radii`** *(list of float, optional)*  
  Provide a custom list of radii instead of generating them statistically. Length must match `num_spheres`.

- **`anisotropy`** *(float, default: 0.0)*  
  Degree of directional distortion applied to the spheres or box shape (e.g., elongation).  
  **Typical range**: `0.0 – 1.0` *(0 = isotropic, 1 = highly stretched)*



<a name="Usage"></a>
# Usage

## Installation

#### From PyPI (Recommended)

```bash
pip install foamify
```

#### From Source

```bash
git clone https://github.com/jackericson98/foamify.git
cd foamify
```

## Running the Program

The general workflow for Foamify is 

1. Configure the parameters
2. Run the program
3. Export the outputs
4. Visualization and analysis

### GUI Operation

With Foamify installed to run the foamify GUI type the following

#### From PyPI 

```bash
python
>>> import foamify
>>> foamify.run()
```

#### From Source
```bash
python foamify
```

The Foamify GUI looks like this. 

### Command line operation


# Dependencies

- Python >= 3.8
- numpy >= 1.21.0
- scipy >= 1.7.0
- matplotlib >= 3.5.0
- numba >= 0.56.0
- pandas >= 1.3.0
- scikit-learn >= 1.0.0

# Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Author

**John Ericson** - Georgia State University (2025), Department of Chemistry

- Email: [jackericson98@gmail.com)[mailto:jackericson98@gmail.com]
- GitHub: [@jackericson98](https://github.com/jackericson98)
- Website: [ericsonlabs.com](https://www.ericsonlabs.com)
- LinkedIn: [John Ericson](https://www.linkedin.com/in/jackericson98/)

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

   
