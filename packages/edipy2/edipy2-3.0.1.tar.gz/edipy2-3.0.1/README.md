# EDIpy2.0: A Python API for the EDIpack2.0 Quantum Impurity Solver
[![api docs](https://img.shields.io/static/v1?label=API&message=documentation&color=734f96&logo=read-the-docs&logoColor=white&style=flat-square)](https://edipack.github.io/EDIpy2.0/)
[![PyPI](https://img.shields.io/pypi/v/edipy2.svg)](https://pypi.org/project/edipy2)
[![Anaconda-Server Badge](https://anaconda.org/edipack/edipack2/badges/version.svg)](https://anaconda.org/edipack/edipack2)

A Python module interfacing to [EDIpack2.0](https://github.com/edipack/EDIpack2.0), 
a  Lanczos based method for the solution of generic Quantum Impurity problems, 
exploiting distributed memory MPI parallelisation. This module offers all the 
features included in EDIpack2.0, solving  *normal*, *superconducting* (s-wave) 
or *Spin-non-conserving* (e.g. with Spin-Orbit Coupling or in-plane magnetization) 
problems, including electron-phonons coupling.

### Install & Use

*EDIpy2.0* is easily installable using pip. It automatically detects and loads the
EDIpack2.0 library using pkg-config. 

### Documentation
All the information about the installation, structure and operation of the module 
is available at [edipack.github.io/EDIpy2.0/](https://edipack.github.io/EDIpy2.0/)  

### Authors
[Lorenzo Crippa](https://github.com/lcrippa)  
[Adriano Amaricci](https://github.com/aamaricci)  


### Issues
If you encounter bugs or difficulties, please 
[file an issue](https://github.com/edipack/EDIpy2.0/issues/new/choose). 
For any other communication, please reach out any of the developers.          
