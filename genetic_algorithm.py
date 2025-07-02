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
    def select_parent_roulette_eight_queen_vector(population: list[list[int]], evaluates: list[int], round: int, randomState: int = None):
        """
        Seleciona os indivíduos que irão reproduzir.

        Args:
            population: Lista de indíviduos aleatórios utilizando a representação de vetor de 8 posições.
            evaluates: Lista com as pontuações dos indivíduos.
            round: Round atual da execução.
            randomState: É o estado definido para a execução.

        Returns:
            Uma lista com os pares de indivíduos selecionados.
        """
        if randomState is not None:
            dynamicSeed = hash((randomState, round)) % (2**32)
            rng = np.random.default_rng(dynamicSeed)
        else: 
            rng = np.random.default_rng()

        numberOfIndividuals = len(population)
        evaluates = 1 / np.array(evaluates)
        choiceProbabilities = np.array(evaluates)/sum(evaluates)

        cumulativeProbabilities = np.cumsum(choiceProbabilities)

        selectedPairs = []
        randomNumbers = rng.random(size=2*len(population))

        for i in range(0, len(randomNumbers), 2):
            firstRandomNumber  = randomNumbers[i]
            firstSelectedIndex = np.searchsorted(cumulativeProbabilities, firstRandomNumber, side="right")
            firstSelectedIndex = min(firstSelectedIndex, numberOfIndividuals - 1)

            secondRandomNumber = randomNumbers[i+1]
            secondSelectedIndex = np.searchsorted(cumulativeProbabilities, secondRandomNumber, side="right")
            secondSelectedIndex = min(secondSelectedIndex, numberOfIndividuals - 1)

            while firstSelectedIndex == secondSelectedIndex:
                secondRandomNumber = rng.random()
                secondSelectedIndex = np.searchsorted(cumulativeProbabilities, secondRandomNumber, side="right")
                secondSelectedIndex = min(secondSelectedIndex, numberOfIndividuals - 1)

            selectedPairs.append((population[firstSelectedIndex], population[secondSelectedIndex]))
            
        return selectedPairs
    
class CrossoverMethods:
    """
    Classe com os métodos de reprodução.
    """
    @staticmethod
    def cut_point_eight_eight_queen_vector(parents: list[tuple[list[int], list[int]]], crossoverRate: float, round: int, randomState: int = None) -> list[list[int]]:
        """
        Reprodução entre os indivíduos utilizando a técnica ponto de corte.

        Args:
            parents: Lista de pares de indíviduos aleatórios selecionados para reprodução.
            crossoverRate: Taxa de cruzamento entre os indivíduos.
            round: É o round atual da execução.
            randomState: É o estado definido para a execução.

        Returns:
            Uma lista com os filhos gerados.
        """

        def generate_sons(firstParent: list[int], secondParent: list[int], rng) -> list[list[int], list[int]]:
            crossover_point = rng.integers(1, len(firstParent))
            first_son = firstParent[:crossover_point] + secondParent[crossover_point:]
            second_son = secondParent[:crossover_point] + firstParent[crossover_point:]
            return [first_son, second_son]

        if randomState is not None:
            dynamicSeed = hash((randomState, round)) % (2**32)
            rng = np.random.default_rng(dynamicSeed)
        else:
            rng = np.random.default_rng()

        sons = []
        numberOfPairs = len(parents)
        randomNumbers = rng.random(size=numberOfPairs)

        for i in range(numberOfPairs):
            if randomNumbers[i] < crossoverRate:
                temporarySons = generate_sons(parents[i][0], parents[i][1], rng)
                sons.append(temporarySons[0])
                sons.append(temporarySons[1])

        return sons
    
class Modifier:
    """
    Classe com os métodos de mutação.
    """
    @staticmethod
    def apply_bit_flip_eight_queen_vector(sons: list[list[int]], mutationRate: float, round: int, randomState: int = None) -> list[list[int]]:
        """
        Gerar mutações nos individuos.

        Args:
            sons: Lista de indíviduos que podem sofrer mutação.
            mutationRate: Taxa de cruzamento entre os indivíduos.
            round: É o round atual da execução.
            randomState: É o estado definido para a execução.

        Returns:
            Uma lista com os filhos mutados ou não.
        """
        def apply_bit_flip(son: list[int], rng):
            mutateSon = son.copy()
            genePosition = rng.integers(0, len(mutateSon))
            geneValue = son[genePosition]

            binaryGene = format(geneValue, '03b')

            bits = list(binaryGene)
            bits[1] = '1' if bits[1] == '0' else '0'

            newValue = int(''.join(bits), 2)
            mutateSon[genePosition] = newValue
            return mutateSon

        if randomState is not None:
            dynamicSeed = hash((randomState, round)) % (2**32)
            rng = np.random.default_rng(dynamicSeed)
        else:
            rng = np.random.default_rng()

        numberOfSons = len(sons)

        for i in range(numberOfSons):
            if rng.random() < mutationRate:
                sons[i] = apply_bit_flip(sons[i], rng)

        return sons
    
class SuvivorCriteria:
    """
    Classe com os métodos de seleção dos sobreviventes.
    """
    @staticmethod
    def random_switch_all_population_eight_queen_vector(oldPopulation: list[list[int]], 
                                                        newPopulation: list[list[int]], 
                                                        oldGenerationEvaluate: list[int], 
                                                        newGenerationEvaluate: list[int],
                                                        populationSize: int,
                                                        round: int,
                                                        randomState: int) -> tuple[list[list[int]], list[int]]:
        """
        Troca toda a geração anterior pela atual, ou seja, só os filhos passam para próxima.

        Args:
            oldPopulation: Lista de indíviduos da geração anterior.
            newPopulation: Lista de indíviduos da geração atual.
            oldGenerationEvaluate: Pontuação da geração anterior.
            newGenerationEvaluate: Pontuação da geração atual.
            populationSize: Número de indivíduos que a população deve ter.
            round: É o round atual da execução.
            randomState: É o estado definido para a execução. 

        Returns:
            Uma lista com os selecionados que irão sobreviver, e a pontuação desses individuos.
        """
        
        if randomState is not None:
            dynamicSeed = hash((randomState, round)) % (2**32)
            rng = np.random.default_rng(dynamicSeed)
        else:
            rng = np.random.default_rng()

        newPopulationSize = len(newPopulation)
        if newPopulationSize >= populationSize:
            selectedIndex = rng.choice(newPopulationSize, size=populationSize, replace=False)
            selectedPopulation = [newPopulation[i] for i in selectedIndex]
            selectedEvaluate = [newGenerationEvaluate[i] for i in selectedIndex]
        else:
            selectedIndex = rng.choice(newPopulationSize, size=newPopulationSize, replace=False)
            selectedPopulation = [newPopulation[i] for i in selectedIndex]
            selectedEvaluate = [newGenerationEvaluate[i] for i in selectedIndex]
            

            selectedPlasterIndex = rng.choice(populationSize, size=(populationSize-newPopulationSize), replace=False)
            selectedPlasterPopulation = [oldPopulation[i] for i in selectedPlasterIndex]
            selectedPlasterEvaluate = [oldGenerationEvaluate[i] for i in selectedIndex]

            selectedPopulation = selectedPopulation + selectedPlasterPopulation
            selectedEvaluate = selectedEvaluate + selectedPlasterEvaluate

        return selectedPopulation, selectedEvaluate
    
    def elitist_replacement_eight_queen_vector(oldPopulation: list[list[int]], 
                                               newPopulation: list[list[int]], 
                                               oldGenerationEvaluate: list[int], 
                                               newGenerationEvaluate: list[int],
                                               populationSize: int) -> tuple[list[list[int]], list[int]]:
        """
        Seleciona somente os melhores individuos, seja parte da geração antiga ou da nova.

        Args:
            oldPopulation: Lista de indíviduos da geração anterior.
            newPopulation: Lista de indíviduos da geração atual.
            oldGenerationEvaluate: Pontuação da geração anterior.
            newGenerationEvaluate: Pontuação da geração atual.
            populationSize: Número de indivíduos que a população deve ter.

        Returns:
            Uma lista com os selecionados que irão sobreviver, e a pontuação desses individuos.
        """

        allIndividuals = oldPopulation + newPopulation
        allScores = oldGenerationEvaluate + newGenerationEvaluate

        paired = sorted(zip(allIndividuals, allScores), key=lambda tupla: tupla[1])

        allIndividualsSorted, allScoresSorted = zip(*paired)

        allIndividualsSorted = list(allIndividualsSorted)
        allScoresSorted = list(allScoresSorted)

        return allIndividualsSorted[:populationSize], allScoresSorted[:populationSize]