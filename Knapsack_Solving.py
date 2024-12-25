import random
import streamlit as st

def knapsack_ga(test_cases):
    results = []
    
    for case_id, (num_items, knapsack_size, items) in enumerate(test_cases, start=1):
        population_size = 100
        generations = 500
        crossover_rate = 0.8
        mutation_rate = 0.01

        # Generate initial population
        population = [[random.randint(0, 1) for _ in range(num_items)] for _ in range(population_size)]

        def fitness(chromosome):
            total_weight = sum(chromosome[i] * items[i][0] for i in range(num_items))
            total_benefit = sum(chromosome[i] * items[i][1] for i in range(num_items))
            return total_benefit if total_weight <= knapsack_size else 0

        def select_parent():
            fitnesses = [fitness(individual) for individual in population]
            total_fitness = sum(fitnesses)
            probabilities = [f / total_fitness for f in fitnesses]
            return population[random.choices(range(population_size), probabilities)[0]]

        def crossover(parent1, parent2):
            if random.random() < crossover_rate:
                point = random.randint(1, num_items - 1)
                return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
            return parent1, parent2

        def mutate(chromosome):
            return [1 - gene if random.random() < mutation_rate else gene for gene in chromosome]

        for generation in range(generations):
            new_population = []
            while len(new_population) < population_size:
                parent1 = select_parent()
                parent2 = select_parent()
                offspring1, offspring2 = crossover(parent1, parent2)
                new_population.extend([mutate(offspring1), mutate(offspring2)])

            population = new_population[:population_size]

        # Get the best solution
        best_chromosome = max(population, key=fitness)
        best_fitness = fitness(best_chromosome)
        selected_items = [items[i] for i in range(num_items) if best_chromosome[i] == 1]

        results.append((case_id, best_fitness, len(selected_items), selected_items))

    return results

# Streamlit app
st.title("Knapsack Problem Solver with Genetic Algorithm")

# Input: Number of test cases
num_cases = st.number_input("Number of test cases", min_value=1, value=1, step=1)

# Define test cases dynamically
test_cases = []
for case_idx in range(num_cases):
    st.subheader(f"Test Case {case_idx + 1}")
    num_items = st.number_input(f"Number of items in Test Case {case_idx + 1}", min_value=1, value=3, step=1, key=f"num_items_{case_idx}")
    knapsack_size = st.number_input(f"Knapsack size in Test Case {case_idx + 1}", min_value=1, value=10, step=1, key=f"knapsack_size_{case_idx}")
    
    items = []
    for item_idx in range(num_items):
        weight = st.number_input(f"Weight of Item {item_idx + 1} (Test Case {case_idx + 1})", min_value=1, value=4, step=1, key=f"weight_{case_idx}_{item_idx}")
        benefit = st.number_input(f"Benefit of Item {item_idx + 1} (Test Case {case_idx + 1})", min_value=1, value=4, step=1, key=f"benefit_{case_idx}_{item_idx}")
        items.append((weight, benefit))
    
    test_cases.append((num_items, knapsack_size, items))

# Run GA and display results
if st.button("Run Genetic Algorithm"):
    results = knapsack_ga(test_cases)
    
    st.header("Results")
    for case_id, total_benefit, num_selected, selected_items in results:
        st.subheader(f"Test Case {case_id}")
        st.write(f"Total Benefit: {total_benefit}")
        st.write(f"Number of Selected Items: {num_selected}")
        st.write("Selected Items (Weight, Benefit):")
        for weight, benefit in selected_items:
            st.write(f"Weight: {weight}, Benefit: {benefit}")
