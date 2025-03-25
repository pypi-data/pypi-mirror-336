from typing import List, Tuple

from ga4qc.circuit import Circuit
from ga4qc.circuit.gates import IGate, Identity
from .interface import IFitness


class WeightedSumFitness(IFitness):
    weights: Tuple[float]

    def __init__(self, weights: Tuple[float]):
        self.weights = weights

    def process(self, circuits: Circuit, generation: int) -> None:
        for circuit in circuits:

            assert len(circuit.fitness_values) == len(
                self.weights), "Mismatch between amount of weights specified and fitness values of circuit."

            fitness = 0
            for obj_i, weight in enumerate(self.weights):
                fitness += weight * circuit.fitness_values[obj_i]

            circuit.fitness_values.append(fitness)
