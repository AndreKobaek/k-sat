# Thesis - Counting homomorphisms and embeddings with \#SAT solvers

This is the repository used for the thesis Counting homomorphisms and embeddings with \#SAT solvers. This repository contains the code required to run the experiments run in thesis as well as producing the results used. The experiments do have crucial dependencies on the presence of the solvers used. These solvers can be installed following the instructions below:

## sharpSAT
The sharpSAT solver can directly cloned from the repository available at https://github.com/marcthurley/sharpSAT into the root folder of this projects' /src folder. The solver can then be built following in the instructions made available in the solvers' repository.
Please confirm that the file sharpSAT has the following path relatively to /src:
../sharpSAT/build/Release/sharpSAT

## GANAK
The GANAK solver can directly cloned from the repository available at https://github.com/meelgroup/ganak into the root folder of this projects' /src folder. The solver can then be built following in the instructions made available in the solvers' repository.
Please confirm that the script run_ganak.sh has the following path relatively to /src:
../ganak/scropts/run_ganak.sh

## HomSub
The HomSub solver can directly cloned from the repository available at https://github.itu.dk/jonmo/SubgraphThesis into the root folder of this projects' /src folder. The solver can then be built following in the instructions made available in the solvers' repository.
Please confirm that the script experiments has the following path relatively to /src:
../SubgraphThesis/experiments-build/experiments/experiments

### Experiments
By running main.py the experiments are executed 
