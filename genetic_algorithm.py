import numpy as np

class PopulationGenerator:
    """
    Classe com os métodos de geração da população.
    """
    @staticmethod
    def generate_eight_queen_vector(numberOfIndividuals: int, randomState: int = None) -> list[list[int]]:
        """
        Gera individuos para o problema das 8 rainhas.
        
        Args:
            numberOfIndividuals: Número de indíviduos que serão gerados.
            randomState: Seed para reprodutibilidade.
        
        Returns:
            Lista de indíviduos aleatórios utilizando a representação de vetor de 8 posições.
        """
        numberOfQueens = 8
        rng = np.random.default_rng(randomState) if randomState is not None else np.random.default_rng()
        return [rng.permutation(numberOfQueens).tolist() for _ in range(numberOfIndividuals)]

class PopulationAssessor:
    """
    Classe com os métodos de avaliação da população.
    """
    @staticmethod
    def evaluate_eight_queen_vector(population: list[list[int]]) -> list[int]:
        """
        Avalia calculando o número de colisões entre os individuos do problema das 8 rainhas.
        
        Args:
            population: Lista de indíviduos aleatórios utilizando a representação de vetor de 8 posições.
        
        Returns:
            Lista contendo a avaliação de cada indíviduo.
        """
        numberOfQueens = len(population[0])
        evaluates = []

        for individual in population:
            collisions = 0
            for column_first in range(numberOfQueens):
                for column_second in range(column_first + 1, numberOfQueens):
                    if abs(column_first - column_second) == abs(individual[column_first] - individual[column_second]):
                        collisions += 1
            evaluates.append(collisions)

        return evaluates
    
class StoppingCriteria:
    """
    Classe com as condições de parada.
    """
    @staticmethod
    def stop_eight_queen_vector_min(evaluates: list[int], minValue: int) -> bool:
        """
        Verifica se o critério de parada foi atendido.
        
        Args:
            evaluates: Lista com as pontuações dos indivíduos.
        
        Returns:
            True ou False.
        """
        return True if minValue in evaluates else False
    
class ParentSelector:
    """
    Classe com os métodos de seleção de pais.
    """
    @staticmethod
    def select_parent_roulette_eight_queen_vector(population: list[list[int]] , evaluates: list[int], crossoverRate: float, round: int, randomState: int = None):
        """
        Seleciona os indivíduos que irão reproduzir.

        Args:
            population: Lista de indíviduos aleatórios utilizando a representação de vetor de 8 posições.

            evaluates: Lista com as pontuações dos indivíduos.

            crossoverRate: Taxa de seleção dos indivíduos.

        Returns:
            Uma lista com os indivíduos selecionados.
        """
        if randomState is not None:
            dynamicSeed = hash((randomState, round)) % (2**32)
            rng = np.random.default_rng(dynamicSeed)
        else: 
            rng = np.random.default_rng()

        numberOfIndividuals = len(population)
        choiceProbabilities = np.array(evaluates)/sum(evaluates)
        numberOfSelections = int(crossoverRate*numberOfIndividuals)
        selectedIndividuals = rng.choice(
            numberOfIndividuals,
            size=numberOfSelections,
            replace=False,
            p=choiceProbabilities
        )
        return [population[i] for i in selectedIndividuals]