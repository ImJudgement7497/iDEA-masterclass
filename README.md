# iDEA-masterclass

## Introduction
This is the repository of all the work done in the Summer 2024 masterclass working on iDEA, supervised by Dr. Matt Hodgson.

All the work was done by Benjamin Mason.

Each directory will contain Jupyter notebooks which should be run to achieve similar results. 

## Particle in a box

For a particle in a box from $0$ to $L$, the energy eigenvalues of a single particle state are given by $\epsilon_{k} = \frac{\pi^{2}}{2L^{2}} (k+1)^2$ in atomic units,for $k = 0, 1, \dots$  with $k = 0$ being the ground state of the system.

The wavefunctions are given by $\psi(x) = \sqrt{\frac{2}{L}}\sin(\frac{(k+1)\pi x}{L})$


## Details on what is in the repoistory

The following is an explanation into each directory:

*`general_comparisons`: Contains data on general comparisons for the particle in a box system, including densities, interacting v non_interacting methods, and small interactions v zero interactions. Data is in the form of notebooks or figures, usually found in a directory called `frames`.

*`index_check`: Contains data on checking the outputs of the package `collections_iDEA` developed during the project. Further information on this package can be found at [collections_iDEA GitHub page](https://github.com/ImJudgement7497/collections_iDEA_package)

*`pib`: Contains data on the majority of the analysis of the particle in a box system. Sub-drectories are distinguished by the number of points used when doing simulations. The most helpful here would be the summary notebooks. The data was collected using `pib_ud_template.py`.

*`qho_231_points`: Contains data on the quantum harmonic oscillator simulations.

*`main_template.py`: The template for the data collection for the general comparisons. Needs to be edited to make sure the parameters are correct for the run that is to be done.

*`methods_template.py`: The methods for the data collection for the general comparisons. Needs to be edited to make sure the parameters are correct for the run that is to be done.
