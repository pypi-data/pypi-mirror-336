# GRAPE: Grammatical Algorithms in Python for Evolution

[GRAPE](https://www.mdpi.com/2624-6120/3/3/39) is an implementation of Grammatical Evolution (GE) in [DEAP](https://deap.readthedocs.io/en/master/), an Evolutionary Computation framework in Python,

## Usage

```python
import grape
from grape import algorithms

BNF_GRAMMAR = grape.Grammar("heartDisease.bnf")

population, logbook = algorithms.ge_eaSimpleWithElitism(
        population,
        toolbox,
        cxpb=P_CROSSOVER,
        mutpb=P_MUTATION,
        ngen=N_GEN,
        elite_size=ELITE_SIZE,
        bnf_grammar=BNF_GRAMMAR,
        codon_size=CODON_SIZE,
        max_tree_depth=MAX_TREE_DEPTH,
        codon_consumption=CODON_CONSUMPTION,
        report_items=REPORT_ITEMS,
        genome_representation=GENOME_REPRESENTATION,
        stats=stats,
        halloffame=hof,
        verbose=False
    )
```

How to cite:

```
Allan de Lima, Samuel Carvalho, Douglas Mota Dias, Enrique Naredo, Joseph P.
Sullivan, and Conor Ryan. 2022. GRAPE: Grammatical Algorithms in Python for
Evolution. Signals 3, 3 (2022), 642–663. https://doi.org/10.3390/signals3030039
```
