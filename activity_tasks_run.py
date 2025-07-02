from genetic_algorithm import *

def run(POPULATION_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE,
        NUMBER_OF_GENERATIONS,
        MIN_VALUE,
        RANDOM_STATE,
        generate_population, 
        evaluate_population, 
        stopping_criterion, 
        parent_selection_strategy, 
        crossover_strategy, 
        mutation_strategy, 
        survivor_selection_strategy,
        return_best_individual_and_score_function):
    """
    Executa o algoritmo genético.

    Args:
        POPULATION_SIZE: Tamanho da população que vai ser gerada.
        CROSSOVER_RATE: Taxa de cruzamento.
        MUTATION_RATE: Taxa de mutação dos filhos.
        NUMBER_OF_GENERATIONS: Número de gerações que serão criadas.
        MIN_VALUE: O valor minimo da função de custo.
        RANDOM_STATE: O estado aleátorio definido.
        generate_population: A função reponsável por gerar a população.
        evaluate_population: A função reponsável por avaliar os individuos.
        stopping_criterion: A função reponsável por verificar se o critério de parada foi atendido.
        parent_selection_strategy: A função reponsável por selecionar os pares para reprodução.
        crossover_strategy: A função reponsável por realizar o cruzamento.
        mutation_strategy: A função reponsável por selecionar alguns filhos e aplicar a mutação dos genes neles.
        survivor_selection_strategy: A função reponsável por selecionar os sobreviventes que irão constituir a próxima geração.
        return_best_individual_and_score_function: A reponsável por selecionar o melhor individuo ao final da execução do código e retornar ele e a sua pontuação.

    Returns:
        O melhor individuo encontrado e o número de execuções.
    """
    
    endRound = 0
    population = generate_population(POPULATION_SIZE, RANDOM_STATE)
    evaluates = evaluate_population(population)

    for round in range(NUMBER_OF_GENERATIONS):
        endRound = round+1

        if stopping_criterion(evaluates, MIN_VALUE) == True:
            break

        parents = parent_selection_strategy(population, evaluates, round, RANDOM_STATE)
        sons = crossover_strategy(parents, CROSSOVER_RATE, round, RANDOM_STATE)
        mutateSons = mutation_strategy(sons, MUTATION_RATE, round, RANDOM_STATE)
        sonsEvaluates = evaluate_population(mutateSons)

        population, evaluates =  survivor_selection_strategy(population, mutateSons, evaluates, sonsEvaluates, POPULATION_SIZE, round, RANDOM_STATE)

    bestIndividual, bestScore = return_best_individual_and_score_function(population, evaluates)

    return bestIndividual, bestScore, endRound

POPULATION_SIZE: int = 20
CROSSOVER_RATE: float = 0.8
MUTATION_RATE:float = 0.03

NUMBER_OF_GENERATIONS: int = 1000
MIN_VALUE: int = 0
RANDOM_STATES: list[int] = [41, 42, 769, 18, 27]
# Individuos distintos que chegaram no 0: 41, 42, 769, 18, 27

def getBestIndividual(individuals: list[list[int]], scores: list[int]) -> list[list[int], int]:
    minValue = min(scores)
    minValueIndex = scores.index(minValue)
    return individuals[minValueIndex], scores[minValueIndex]

print("\nTask, c) As 5 melhores soluções distintas encontradas:")

for RANDOM_STATE in RANDOM_STATES:
    bestIndividual, bestScore, endRound = run(POPULATION_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE,
        NUMBER_OF_GENERATIONS,
        MIN_VALUE,
        RANDOM_STATE,
        generate_population = PopulationGenerator.generate_eight_queen_vector,
        evaluate_population = PopulationAssessor.evaluate_eight_queen_vector, 
        stopping_criterion = StoppingCriteria.stop_eight_queen_vector_min,
        parent_selection_strategy = ParentSelector.select_parent_roulette_eight_queen_vector,
        crossover_strategy = CrossoverMethods.cut_point_eight_eight_queen_vector,
        mutation_strategy = Modifier.apply_bit_flip_eight_queen_vector,
        survivor_selection_strategy = SuvivorCriteria.random_switch_all_population_eight_queen_vector,
        return_best_individual_and_score_function = getBestIndividual)

    print(f"Melhor individuo: {bestIndividual} | Pontuação: {bestScore} | Encontrado no round: {endRound}")

print("\nTask, b) A média e o desvio-padrão do número de iterações até a parada do algoritmo:")

import numpy as np
from random import randint
from time import time

numberOfExecutions = 5000
maxRandomState = 2**32
printRound = 50

results = {
    "Individuals" : [],
    "Scores" : [],
    "End Rounds" : [],
    "Execution Times" : []
}

roundCounter = 1
for RANDOM_STATE in [randint(0, maxRandomState) for _ in range(numberOfExecutions)]:
    if roundCounter % printRound == 0:
        print(f"Round: {roundCounter}")
    roundCounter += 1

    startTime = time()

    bestIndividual, bestScore, endRound = run(POPULATION_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE,
        NUMBER_OF_GENERATIONS,
        MIN_VALUE,
        RANDOM_STATE,
        generate_population = PopulationGenerator.generate_eight_queen_vector,
        evaluate_population = PopulationAssessor.evaluate_eight_queen_vector, 
        stopping_criterion = StoppingCriteria.stop_eight_queen_vector_min,
        parent_selection_strategy = ParentSelector.select_parent_roulette_eight_queen_vector,
        crossover_strategy = CrossoverMethods.cut_point_eight_eight_queen_vector,
        mutation_strategy = Modifier.apply_bit_flip_eight_queen_vector,
        survivor_selection_strategy = SuvivorCriteria.random_switch_all_population_eight_queen_vector,
        return_best_individual_and_score_function = getBestIndividual)

    results["Individuals"].append(bestIndividual)
    results["Scores"].append(bestScore)
    results["End Rounds"].append(endRound)
    results["Execution Times"].append(time() - startTime)

print(f"\nO número de execuções foi: {numberOfExecutions}")
print(f"|- Número médio de gerações: {np.mean(results['End Rounds']):.2f} | Desvio padrão no número de gerações: {np.std(results['End Rounds']):.2f}")
print(f"|- Tempo médio de execução: {np.mean(results['Execution Times']):.2f} | Desvio padrão no tempo de execução: {np.std(results['Execution Times']):.2f}")