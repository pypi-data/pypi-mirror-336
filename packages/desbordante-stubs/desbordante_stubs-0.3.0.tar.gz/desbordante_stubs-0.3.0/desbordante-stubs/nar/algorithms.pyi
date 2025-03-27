from __future__ import annotations
import desbordante.nar

__all__ = ["DES", "Default"]

class DES(desbordante.nar.NarAlgorithm):
    """
    Options:
    table: table processed by the algorithm
    differential_strategy: DES mutation strategy to use
    [rand1Bin|rand1Exp|randToBest1Exp|best2Exp|rand2Exp|best1Bin|best1Exp|randToBest1Bin|best2Bin|rand2Bin]
    seed: RNG seed
    minconf: minimum confidence value (between 0 and 1)
    minsup: minimum support value (between 0 and 1)
    population_size: the number of individuals in the population at any given time
    max_fitness_evaluations: the algorithm will be stopped after calculating the fitness function this many times
    differential_scale: the magnitude of mutations
    crossover_probability: probability of a gene getting mutated in a new individual
    """
    def __init__(self) -> None: ...

Default = DES
