# Connectome Analysis

#### General functions to analyze connectomes from a topological perspective.  

![](docs/banner_BPP_connalysis.jpg)

---

## Documentation 

See our [**documentation**](https://openbraininstitute.github.io/connectome-analysis/) for detailed explanations including examples and tutorials.

See our [**source code**](src/connalysis) for implementation details.

## User installation

```sh
pip install git+https://github.com/openbraininstitute/connectome-analysis.git
```

---

## Citation  

[![DOI:10.1101/2024.03.15.585196](http://img.shields.io/badge/DOI-10.1101/2024.03.15.585196-B31B1B.svg)](https://doi.org/10.1101/2024.03.15.585196)

If you use this software, kindly use the following BibTeX entry for citation:

```
@article{egas2024efficiency,
  title={Efficiency and reliability in biological neural network architectures},
  author={Egas Santander, Daniela and Pokorny, Christoph and Ecker, Andr{\'a}s and Lazovskis, J{\=a}nis and Santoro, Matteo and Smith, Jason P and Hess, Kathryn and Levi, Ran and Reimann, Michael W},
  journal={bioRxiv},
  pages={2024--03},
  year={2024},
  publisher={Cold Spring Harbor Laboratory},
  doi = {10.1101/2024.03.15.585196}
}
```

---
## Acknowledgements & Funding

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology.

Copyright (c) 2023-2024 Blue Brain Project / EPFL.<br>
Copyright (c) 2025 Open Brain Institute.

---

## Development installation

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * [gcc](https://gcc.gnu.org/) 9+
  * [CMake](https://cmake.org/)
  * Python 3.9+

* Create a virtual environment and install the dependencies

```sh
poetry install
```

CMake may have difficulties to find the right compilers to compile the C++ code. 
If that is the case, you have to specify the path to the compilers yourself:

```sh
CC=/path/to/gcc CXX=/path/to/g++ poetry install
```

This is especially important on MacOS.

* Activate the virtual environment

```sh
poetry shell
```

* Testing

```sh
poetry run pytest tests
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.
