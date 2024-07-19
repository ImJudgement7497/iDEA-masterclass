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

-`general_comparisons`: Contains data on general comparisons for the particle in a box system, including densities, interacting v non_interacting methods, and small interactions v zero interactions. Data is in the form of notebooks or figures, usually found in a directory called `frames`.

-`index_check`: Contains data on checking the outputs of the package `collections_iDEA` developed during the project. Further information on this package can be found at [collections_iDEA GitHub page](https://github.com/ImJudgement7497/collections_iDEA_package)

-`pib`: Contains data on the majority of the analysis of the particle in a box system. Sub-drectories are distinguished by the number of points used when doing simulations. The most helpful here would be the summary notebooks. The data was collected using `pib_ud_template.py`.

-`qho_231_points`: Contains data on the quantum harmonic oscillator simulations for 231 points.

-`qho_350_points`: Contains data on the quantum harmonic oscillator simulations for 350 points.

-`qho_uu`: Contains data on the quantum harmonic oscillator simulations for an `uu` system.

-`testing`: Contains some scripts to test the initalisation of `iDEA` and `collections_iDEA`.

-`main_template.py`: The template for the data collection for the general comparisons. Needs to be edited to make sure the parameters are correct for the run that is to be done.

-`methods_template.py`: The methods for the data collection for the general comparisons. Needs to be edited to make sure the parameters are correct for the run that is to be done.

## Main findings

During the course of the project, my aim was to test the reliability of iDEA's output of multiplet states. I have met this aim as well as a few others.

Initally I started to look at a particle in a box system, and test that `iDEA.methods.non_interacting` was outputting the correct energies and that when we called `iDEA.methods.interacting` for a two body system, but the interaction set to 0, it was producing the correct energy orderings. I found that iDEA was reliable, however that a particle in a box system was incredibly hard for iDEA to converge. This is due to there being no external potential in the system, so the infinte boundary conditions presented a huge issue. When considering the probability densities of these excited states of a single body system, we found that iDEA was outputting the data on a grid differently to how the analytic data was being outputted. However implementing a simple fix of adding two extra grid points to the analytic data, then slicing them off, improved this significantly. 

I moved on to making sure iDEA's `interacting` and `non_interacting` method was outputting the same energy for when the interaction was set to 0. I found that they were the same. The probability densities for a many body system were checked for a high number of excited states and the results were as expected. I used my package `collections_iDEA` to find analytic results for this system and compared them to iDEA's outputs. If work like this continues however, it is important to note that the indexing provided by `collections_iDEA` compared to `iDEA` may not always match up at multiplets, due to the innate degeneracy. This means that some data may not match (see file `120_diff.png` in `\general_comparisons\densities\frames`). This is because at multiplets, the index ordering is completley arbitary. However there is always a matching pair for this system.

In terms of multiplets, iDEA was reliably producing the expected number of multiplets for a high number of excited states. There is some discrepency at excited state 99, however this has not been fully explored. 

All my work on particle in a box can be found in `pib`. I also did a presentation on this as part of my project, whch can be found [here](https://youtu.be/qYbEzCIr1XQ). However due to the nature of the system, and how hard iDEA has to work to get results, I highly recommend not using this system.

I moved on to a quantum harmonic oscillator system, to match my peers, and also provide aid in their work of creating numerical tests. I did similar analysis for QHO and found expected behaviour for an `ud` system, energies at no interaction match energies when the interactiong tends to 0, and the probability densities match up to expected behaviour. For multiplets, for all the mulitiplets to match expected behaviour, the tolerance for comparing if energies are degenerate needs to be ~0.08 which is quite a large error, however for higher and higher excited states, numercal noise becomes quite apparent. 

A system of `uu` particles however....

## Recommendations to others

Below is a list of recommendations, some of which may prove useful when you start tinkering with iDEA.

- Set up a GitHub repository to keep a backup of your work: GitHub is a very good place to keep code safe, and VS Code provides an easy method on how to commit and push data to your own repository. 

- When doing simulations, always save your state object to a file: There were countless times where I would do a run that may take a couple of hours to get some specifc data, only to need some part else aswel and have to do the run again. I recommend saving your state objects to a `pickle` file, so all available information is saved.

- Try best to comment code that may be seen by other people: It is helpful to everyone if there are comments or doc strings that explain.

- Use `collections_iDEA`: The package I developed provides a centralised way of dealing with many states at once, and peform similar analysis on those states in one package. If I made it at the start of my project, it would help cut down on lots of time tinkering with code and more time analysisng results.

