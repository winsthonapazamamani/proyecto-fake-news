import numpy as np
import random
import time
from typing import List, Dict, Any, Tuple
from sklearn.metrics import accuracy_score
import json
from .database import get_db

class GeneticAlgorithmOptimizer:
    def __init__(self, population_size=30, generations=50, mutation_rate=0.1):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        
        # Espacio de busqueda para hiperparametros
        self.parameter_space = {
            'learning_rate': [0.001, 0.01, 0.1],
            'hidden_units': [32, 64, 128, 256],
            'dropout_rate': [0.2, 0.3, 0.5],
            'batch_size': [16, 32, 64],
            'optimizer': ['adam', 'rmsprop']
        }
    
    def create_individual(self) -> Dict[str, Any]:
        """Crear un individuo aleatorio"""
        individual = {}
        for param, values in self.parameter_space.items():
            individual[param] = random.choice(values)
        return individual
    
    def fitness_function(self, individual: Dict[str, Any]) -> float:
        """
        Funcion de fitness - Simula performance del modelo
        En produccion, esto entrenaria un modelo real
        """
        score = 0.0
        
        # Learning rate optimo
        if individual['learning_rate'] == 0.001:
            score += 0.3
        elif individual['learning_rate'] == 0.01:
            score += 0.2
        
        # Unidades ocultas
        hidden_units_score = min(individual['hidden_units'] / 256, 0.3)
        score += hidden_units_score
        
        # Dropout
        if individual['dropout_rate'] == 0.3:
            score += 0.2
        
        # Optimizer
        if individual['optimizer'] == 'adam':
            score += 0.2
        
        # Aleatoriedad controlada
        score += random.uniform(0, 0.1)
        
        return min(score, 1.0)
    
    def optimize(self) -> Dict[str, Any]:
        """Ejecutar algoritmo genetico"""
        print("Ejecutando Algoritmo Genetico...")
        start_time = time.time()
        
        # Inicializar poblacion
        population = [self.create_individual() for _ in range(self.population_size)]
        best_individual = None
        best_fitness = -1
        history = []
        
        for generation in range(self.generations):
            # Evaluar fitness
            fitness_scores = [self.fitness_function(ind) for ind in population]
            
            # Encontrar el mejor
            current_best_idx = np.argmax(fitness_scores)
            current_best_fitness = fitness_scores[current_best_idx]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = population[current_best_idx]
            
            history.append({
                'generation': generation,
                'best_fitness': best_fitness,
                'avg_fitness': np.mean(fitness_scores)
            })
            
            # Seleccion (ruleta)
            total_fitness = sum(fitness_scores)
            probabilities = [score / total_fitness for score in fitness_scores]
            selected = random.choices(population, weights=probabilities, k=self.population_size)
            
            # Cruzamiento y mutacion
            new_population = []
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    parent1, parent2 = selected[i], selected[i + 1]
                    
                    # Cruzamiento de un punto
                    child1, child2 = parent1.copy(), parent2.copy()
                    crossover_point = random.choice(list(self.parameter_space.keys()))
                    child1[crossover_point], child2[crossover_point] = child2[crossover_point], child1[crossover_point]
                    
                    # Mutacion
                    if random.random() < self.mutation_rate:
                        param_to_mutate = random.choice(list(self.parameter_space.keys()))
                        child1[param_to_mutate] = random.choice(self.parameter_space[param_to_mutate])
                    
                    if random.random() < self.mutation_rate:
                        param_to_mutate = random.choice(list(self.parameter_space.keys()))
                        child2[param_to_mutate] = random.choice(self.parameter_space[param_to_mutate])
                    
                    new_population.extend([child1, child2])
            
            population = new_population
        
        duration = time.time() - start_time
        
        # Guardar resultados
        self.save_optimization_result('genetic_algorithm', best_fitness, best_individual, duration)
        
        print(f"AG completado en {duration:.2f}s - Mejor fitness: {best_fitness:.4f}")
        
        return {
            'method': 'genetic_algorithm',
            'best_score': best_fitness,
            'best_params': best_individual,
            'duration': duration,
            'iterations': self.generations,
            'history': history
        }
    
    def save_optimization_result(self, method, best_score, best_params, duration):
        """Guardar resultado de optimizacion"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO optimizations (method, best_score, parameters, duration) VALUES (?, ?, ?, ?)",
                    (method, best_score, json.dumps(best_params), duration)
                )
                conn.commit()
        except Exception as e:
            print(f"Error guardando optimizacion: {e}")

class ParticleSwarmOptimizer:
    def __init__(self, num_particles=20, max_iterations=50):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        
        # Espacio de busqueda continuo
        self.parameter_bounds = {
            'learning_rate': (0.0001, 0.1),
            'hidden_units': (16, 256),
            'dropout_rate': (0.1, 0.7)
        }
        
        self.param_names = list(self.parameter_bounds.keys())
    
    def optimize(self) -> Dict[str, Any]:
        """Ejecutar PSO"""
        print("Ejecutando Particle Swarm Optimization...")
        start_time = time.time()
        
        # Inicializar particulas
        particles = np.random.uniform(
            low=[self.parameter_bounds[p][0] for p in self.param_names],
            high=[self.parameter_bounds[p][1] for p in self.param_names],
            size=(self.num_particles, len(self.param_names))
        )
        
        velocities = np.random.uniform(-1, 1, particles.shape)
        personal_best_positions = particles.copy()
        personal_best_scores = np.zeros(self.num_particles)
        
        # Parametros PSO
        w = 0.7  # inercia
        c1 = 1.4  # cognitivo
        c2 = 1.4  # social
        
        global_best_position = None
        global_best_score = -1
        history = []
        
        for iteration in range(self.max_iterations):
            for i in range(self.num_particles):
                # Convertir particula a parametros
                params = {
                    self.param_names[j]: particles[i][j] 
                    for j in range(len(self.param_names))
                }
                
                # Discretizar algunos parametros
                if 'hidden_units' in params:
                    params['hidden_units'] = int(params['hidden_units'])
                
                # Evaluar fitness
                score = self.fitness_function(params)
                
                # Actualizar mejores posiciones
                if score > personal_best_scores[i]:
                    personal_best_scores[i] = score
                    personal_best_positions[i] = particles[i].copy()
                    
                    if score > global_best_score:
                        global_best_score = score
                        global_best_position = particles[i].copy()
            
            # Actualizar velocidades y posiciones
            for i in range(self.num_particles):
                r1, r2 = np.random.random(), np.random.random()
                
                cognitive = c1 * r1 * (personal_best_positions[i] - particles[i])
                social = c2 * r2 * (global_best_position - particles[i])
                
                velocities[i] = w * velocities[i] + cognitive + social
                particles[i] += velocities[i]
                
                # Aplicar limites
                for j in range(len(self.param_names)):
                    low, high = self.parameter_bounds[self.param_names[j]]
                    particles[i][j] = np.clip(particles[i][j], low, high)
            
            history.append({
                'iteration': iteration,
                'best_score': global_best_score,
                'avg_score': np.mean(personal_best_scores)
            })
        
        duration = time.time() - start_time
        
        # Convertir mejor posicion a parametros
        best_params = {
            self.param_names[i]: float(global_best_position[i])
            for i in range(len(self.param_names))
        }
        if 'hidden_units' in best_params:
            best_params['hidden_units'] = int(best_params['hidden_units'])
        
        self.save_optimization_result('particle_swarm', global_best_score, best_params, duration)
        
        print(f"PSO completado en {duration:.2f}s - Mejor fitness: {global_best_score:.4f}")
        
        return {
            'method': 'particle_swarm',
            'best_score': global_best_score,
            'best_params': best_params,
            'duration': duration,
            'iterations': self.max_iterations,
            'history': history
        }
    
    def fitness_function(self, params):
        """Funcion de fitness para PSO"""
        score = 0.0
        
        if 0.001 <= params.get('learning_rate', 0) <= 0.01:
            score += 0.3
        
        if params.get('hidden_units', 0) >= 64:
            score += 0.3
        
        if 0.2 <= params.get('dropout_rate', 0) <= 0.5:
            score += 0.2
        
        score += random.uniform(0, 0.2)
        
        return min(score, 1.0)
    
    def save_optimization_result(self, method, best_score, best_params, duration):
        """Guardar resultado de optimizacion"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO optimizations (method, best_score, parameters, duration) VALUES (?, ?, ?, ?)",
                    (method, best_score, json.dumps(best_params), duration)
                )
                conn.commit()
        except Exception as e:
            print(f"Error guardando optimizacion PSO: {e}")

class SimulatedAnnealingOptimizer:
    def __init__(self, initial_temperature=1000, cooling_rate=0.95):
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        
        self.parameter_space = {
            'learning_rate': [0.001, 0.01, 0.1],
            'hidden_units': [32, 64, 128, 256],
            'dropout_rate': [0.2, 0.3, 0.5],
            'batch_size': [16, 32, 64]
        }
    
    def optimize(self) -> Dict[str, Any]:
        """Ejecutar Simulated Annealing"""
        print("Ejecutando Simulated Annealing...")
        start_time = time.time()
        
        # Solucion inicial
        current_solution = self.create_random_solution()
        current_score = self.fitness_function(current_solution)
        
        best_solution = current_solution.copy()
        best_score = current_score
        
        temperature = self.initial_temperature
        history = []
        iteration = 0
        
        while temperature > 1:
            # Generar vecino
            neighbor = self.get_neighbor(current_solution)
            neighbor_score = self.fitness_function(neighbor)
            
            # Calcular probabilidad de aceptacion
            if neighbor_score > current_score:
                acceptance_prob = 1.0
            else:
                acceptance_prob = np.exp((neighbor_score - current_score) / temperature)
            
            # Aceptar o rechazar
            if acceptance_prob > random.random():
                current_solution = neighbor
                current_score = neighbor_score
                
                if current_score > best_score:
                    best_solution = current_solution.copy()
                    best_score = current_score
            
            history.append({
                'iteration': iteration,
                'temperature': temperature,
                'current_score': current_score,
                'best_score': best_score
            })
            
            # Enfriar
            temperature *= self.cooling_rate
            iteration += 1
        
        duration = time.time() - start_time
        
        self.save_optimization_result('simulated_annealing', best_score, best_solution, duration)
        
        print(f"SA completado en {duration:.2f}s - Mejor fitness: {best_score:.4f}")
        
        return {
            'method': 'simulated_annealing',
            'best_score': best_score,
            'best_params': best_solution,
            'duration': duration,
            'iterations': iteration,
            'history': history
        }
    
    def create_random_solution(self):
        """Crear solucion aleatoria"""
        solution = {}
        for param, values in self.parameter_space.items():
            solution[param] = random.choice(values)
        return solution
    
    def get_neighbor(self, solution):
        """Generar solucion vecina"""
        neighbor = solution.copy()
        param_to_change = random.choice(list(self.parameter_space.keys()))
        current_value = neighbor[param_to_change]
        possible_values = [v for v in self.parameter_space[param_to_change] if v != current_value]
        
        if possible_values:
            neighbor[param_to_change] = random.choice(possible_values)
        
        return neighbor
    
    def fitness_function(self, solution):
        """Funcion de fitness para SA"""
        score = 0.0
        
        if solution['learning_rate'] == 0.001:
            score += 0.3
        
        if solution['hidden_units'] >= 64:
            score += 0.3
        
        if solution['dropout_rate'] == 0.3:
            score += 0.2
        
        score += random.uniform(0, 0.2)
        
        return min(score, 1.0)
    
    def save_optimization_result(self, method, best_score, best_params, duration):
        """Guardar resultado de optimizacion"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO optimizations (method, best_score, parameters, duration) VALUES (?, ?, ?, ?)",
                    (method, best_score, json.dumps(best_params), duration)
                )
                conn.commit()
        except Exception as e:
            print(f"Error guardando optimizacion SA: {e}")

class Optimizer:
    """Clase principal de optimizacion"""
    
    def __init__(self):
        self.genetic_optimizer = GeneticAlgorithmOptimizer()
        self.pso_optimizer = ParticleSwarmOptimizer()
        self.sa_optimizer = SimulatedAnnealingOptimizer()
    
    def optimize(self, method="genetic"):
        """Ejecutar optimizacion con metodo especifico"""
        if method == "genetic":
            return self.genetic_optimizer.optimize()
        elif method == "pso":
            return self.pso_optimizer.optimize()
        elif method == "annealing":
            return self.sa_optimizer.optimize()
        else:
            raise ValueError(f"Metodo no soportado: {method}")

# Instancia global del optimizador
optimizer = Optimizer()