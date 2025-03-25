# EDIpy2.0: A Python API for the EDIpack2.0 Quantum Impurity Solver

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
