from genetic_algorithm import *

POPULATION_SIZE: int = 20
CROSSOVER_RATE: float = 0.8
MUTATION_RATE:float = 0.03

NUMBER_OF_GENERATIONS: int = 1000
MIN_VALUE: int = 0
RANDOM_STATE: int = 42
# Individuos distintos que chegaram no 0: 41, 42, 769, 18, 27, 89, 746
# 41 termina de primeira, 42 é o que eu uso pra testar

generate_population = PopulationGenerator.generate_eight_queen_vector
evaluate_population = PopulationAssessor.evaluate_eight_queen_vector 
stopping_criterion = StoppingCriteria.stop_eight_queen_vector_min
parent_selection_strategy = ParentSelector.select_parent_roulette_eight_queen_vector
crossover_strategy = CrossoverMethods.cut_point_eight_eight_queen_vector
mutation_strategy = Modifier.apply_bit_flip_eight_queen_vector
survivor_selection_strategy = SuvivorCriteria.random_switch_all_population_eight_queen_vector


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

print(f"\nPopulação Final alcançada no round {endRound}, número de indivíduos: {len(population)}:")
for i in range(len(population)):
    print(f"Indivíduo: {population[i]} | Pontuação: {evaluates[i]}")

print()