"""
遗传算法引擎 - 实现旋律进化的选择/交叉/变异/精英保留功能
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Callable
import random
import math
import copy
from enum import Enum

from .melody import MelodyConfig, MelodyState, EmotionType
from .fitness import MelodyFitnessEvaluator, FitnessScore
from .scales import Scale, ScaleType, ScaleFactory
from .notes import NoteName


class SelectionType(Enum):
    """选择类型"""
    TOURNAMENT = "tournament"
    ROULETTE_WHEEL = "roulette_wheel"
    RANK = "rank"
    ELITE = "elite"


class CrossoverType(Enum):
    """交叉类型"""
    SINGLE_POINT = "single_point"
    UNIFORM = "uniform"
    BLEND = "blend"


class MutationType(Enum):
    """变异类型"""
    PITCH = "pitch"
    RHYTHM = "rhythm"
    DYNAMIC = "dynamic"
    STRUCTURE = "structure"


@dataclass
class MelodyIndividual:
    """旋律个体 - 基因编码表示"""
    melody_states: List[MelodyState] = field(default_factory=list)
    fitness: float = 0.0
    generation: int = 0
    parent_ids: Tuple[int, int] = (0, 0)  # 父代ID
    
    def __post_init__(self):
        """初始化后处理"""
        if not self.melody_states:
            self.fitness = 0.0
        else:
            # 计算适应度
            self.fitness = self.calculate_fitness()
    
    def calculate_fitness(self, evaluator: Optional[MelodyFitnessEvaluator] = None) -> float:
        """计算适应度"""
        if not evaluator:
            # 使用默认评估器
            scale = ScaleFactory.create_scale(NoteName.C, "major")
            evaluator = MelodyFitnessEvaluator(scale)
        
        if not self.melody_states:
            return 0.0
        
        fitness_score = evaluator.evaluate_fitness(self.melody_states)
        return fitness_score.total_score
    
    def get_gene_info(self) -> Dict:
        """获取基因信息用于调试"""
        if not self.melody_states:
            return {}
        
        pitch_genes = []
        rhythm_genes = []
        dynamic_genes = []
        
        for i, state in enumerate(self.melody_states):
            # 音高基因
            pitch_genes.append({
                'note': str(state.note.name),
                'octave': state.octave,
                'degree': state.note_degree if hasattr(state, 'note_degree') else 0,
                'position': i / len(self.melody_states)
            })
            
            # 节奏基因
            rhythm_genes.append({
                'duration': state.duration,
                'position': i / len(self.melody_states),
                'beat_strength': getattr(state, 'beat_strength', 0.8)
            })
            
            # 力度基因
            dynamic_genes.append({
                'velocity': getattr(state, 'velocity', 80),
                'accent': getattr(state, 'accent', 1.0)
            })
        
        return {
            'pitch_genes': pitch_genes,
            'rhythm_genes': rhythm_genes,
            'dynamic_genes': dynamic_genes,
            'fitness': self.fitness,
            'generation': self.generation,
            'parent_ids': self.parent_ids
        }


class SelectionOperator:
    """选择操作器"""
    
    def __init__(self, selection_type: SelectionType = SelectionType.TOURNAMENT, 
                 tournament_size: int = 3):
        self.selection_type = selection_type
        self.tournament_size = tournament_size
    
    def select(self, population: List[MelodyIndividual]) -> MelodyIndividual:
        """从种群中选择个体"""
        if not population:
            raise ValueError("Population is empty")
        
        if len(population) == 1:
            return population[0]
        
        if self.selection_type == SelectionType.TOURNAMENT:
            return self._tournament_selection(population)
        elif self.selection_type == SelectionType.ROULETTE_WHEEL:
            return self._roulette_wheel_selection(population)
        elif self.selection_type == SelectionType.RANK:
            return self._rank_selection(population)
        elif self.selection_type == SelectionType.ELITE:
            return self._elite_selection(population)
        else:
            raise ValueError(f"Unknown selection type: {self.selection_type}")
    
    def _tournament_selection(self, population: List[MelodyIndividual]) -> MelodyIndividual:
        """锦标赛选择"""
        # 随机选择tournament_size个个体进行竞争
        tournament = random.sample(population, min(self.tournament_size, len(population)))
        # 返回适应度最高的个体
        return max(tournament, key=lambda ind: ind.fitness)
    
    def _roulette_wheel_selection(self, population: List[MelodyIndividual]) -> MelodyIndividual:
        """轮盘赌选择"""
        # 计算总适应度
        total_fitness = sum(ind.fitness for ind in population)
        if total_fitness == 0:
            # 如果所有个体适应度都为0，随机选择
            return random.choice(population)
        
        # 根据适应度比例选择
        pick = random.uniform(0, total_fitness)
        current = 0
        
        for individual in population:
            current += individual.fitness
            if current >= pick:
                return individual
        
        # 如果由于浮点精度问题没有选中，返回最后一个
        return population[-1]
    
    def _rank_selection(self, population: List[MelodyIndividual]) -> MelodyIndividual:
        """排序选择"""
        # 按适应度排序
        sorted_pop = sorted(population, key=lambda ind: ind.fitness, reverse=True)
        # 生成排名权重
        ranks = list(range(1, len(sorted_pop) + 1))
        probabilities = [1/r for r in ranks]
        probabilities = [p/sum(probabilities) for p in probabilities]
        # 按权重选择
        return random.choices(sorted_pop, weights=probabilities, k=1)[0]
    
    def _elite_selection(self, population: List[MelodyIndividual]) -> MelodyIndividual:
        """精英选择"""
        return max(population, key=lambda ind: ind.fitness)


class CrossoverOperator:
    """交叉操作器"""
    
    def __init__(self, crossover_type: CrossoverType = CrossoverType.SINGLE_POINT):
        self.crossover_type = crossover_type
    
    def crossover(self, parent1: MelodyIndividual, parent2: MelodyIndividual) -> Tuple[MelodyIndividual, MelodyIndividual]:
        """交叉生成两个子代"""
        if self.crossover_type == CrossoverType.SINGLE_POINT:
            return self._single_point_crossover(parent1, parent2)
        elif self.crossover_type == CrossoverType.UNIFORM:
            return self._uniform_crossover(parent1, parent2)
        elif self.crossover_type == CrossoverType.BLEND:
            return self._blend_crossover(parent1, parent2)
        else:
            raise ValueError(f"Unknown crossover type: {self.crossover_type}")
    
    def _single_point_crossover(self, parent1: MelodyIndividual, parent2: MelodyIndividual) -> Tuple[MelodyIndividual, MelodyIndividual]:
        """单点交叉"""
        crossover_point = random.randint(1, len(parent1.melody_states) - 1)
        
        child1 = MelodyIndividual(
            melody_states=parent1.melody_states[:crossover_point] + parent2.melody_states[crossover_point:],
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=(id(parent1), id(parent2))
        )
        
        child2 = MelodyIndividual(
            melody_states=parent2.melody_states[:crossover_point] + parent1.melody_states[crossover_point:],
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=(id(parent2), id(parent1))
        )
        
        return child1, child2
    
    def _uniform_crossover(self, parent1: MelodyIndividual, parent2: MelodyIndividual) -> Tuple[MelodyIndividual, MelodyIndividual]:
        """均匀交叉"""
        child1_states = []
        child2_states = []
        
        for i in range(len(parent1.melody_states)):
            if random.random() < 0.5:
                child1_states.append(copy.deepcopy(parent1.melody_states[i]))
                child2_states.append(copy.deepcopy(parent2.melody_states[i]))
            else:
                child1_states.append(copy.deepcopy(parent2.melody_states[i]))
                child2_states.append(copy.deepcopy(parent1.melody_states[i]))
        
        child1 = MelodyIndividual(
            melody_states=child1_states,
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=(id(parent1), id(parent2))
        )
        
        child2 = MelodyIndividual(
            melody_states=child2_states,
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=(id(parent2), id(parent1))
        )
        
        return child1, child2
    
    def _blend_crossover(self, parent1: MelodyIndividual, parent2: MelodyIndividual) -> Tuple[MelodyIndividual, MelodyIndividual]:
        """混合交叉（对数值型基因进行混合）"""
        child1_states = []
        child2_states = []
        
        for i in range(len(parent1.melody_states)):
            state1 = parent1.melody_states[i]
            state2 = parent2.melody_states[i]
            
            # 创建混合状态
            blended_state1 = copy.deepcopy(state1)
            blended_state2 = copy.deepcopy(state2)
            
            # 混合数值型属性
            # 八度混合
            blended_octave1 = int((state1.octave + state2.octave) / 2)
            blended_octave2 = blended_octave1
            blended_state1.octave = blended_octave1
            blended_state2.octave = blended_octave2
            
            # 时值混合
            blended_duration1 = (state1.duration + state2.duration) / 2
            blended_duration2 = blended_duration1
            blended_state1.duration = blended_duration1
            blended_state2.duration = blended_duration2
            
            # 力度混合
            if hasattr(state1, 'velocity') and hasattr(state2, 'velocity'):
                blended_velocity1 = int((state1.velocity + state2.velocity) / 2)
                blended_velocity2 = blended_velocity1
                blended_state1.velocity = blended_velocity1
                blended_state2.velocity = blended_velocity2
            
            child1_states.append(blended_state1)
            child2_states.append(blended_state2)
        
        child1 = MelodyIndividual(
            melody_states=child1_states,
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=(id(parent1), id(parent2))
        )
        
        child2 = MelodyIndividual(
            melody_states=child2_states,
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=(id(parent2), id(parent1))
        )
        
        return child1, child2


class MutationOperator:
    """变异操作器"""
    
    def __init__(self, mutation_rate: float = 0.1, mutation_strength: float = 0.3):
        self.mutation_rate = mutation_rate  # 变异概率
        self.mutation_strength = mutation_strength  # 变异强度
    
    def mutate(self, individual: MelodyIndividual) -> MelodyIndividual:
        """变异个体"""
        mutated_states = []
        
        for i, state in enumerate(individual.melody_states):
            mutated_state = copy.deepcopy(state)
            
            # 音高变异
            if random.random() < self.mutation_rate:
                mutated_state = self._pitch_mutation(mutated_state)
            
            # 节奏变异
            if random.random() < self.mutation_rate:
                mutated_state = self._rhythm_mutation(mutated_state)
            
            # 力度变异
            if random.random() < self.mutation_rate:
                mutated_state = self._dynamic_mutation(mutated_state)
            
            # 结构变异（低概率，因为影响较大）
            if random.random() < self.mutation_rate * 0.3:
                mutated_state = self._structure_mutation(mutated_state, i / len(individual.melody_states))
            
            mutated_states.append(mutated_state)
        
        return MelodyIndividual(
            melody_states=mutated_states,
            generation=individual.generation + 1,
            parent_ids=(individual.parent_ids[0], individual.parent_ids[1])
        )
    
    def _pitch_mutation(self, state: MelodyState) -> MelodyState:
        """音高变异"""
        # 音符变异
        if random.random() < 0.3:  # 30%概率变异音符
            from .notes import NoteName
            state.note = random.choice(list(NoteName))
        
        # 八度变异
        if random.random() < 0.2:  # 20%概率变异八度
            state.octave = max(1, min(8, state.octave + random.randint(-1, 1)))
        
        # 音阶度数变异
        if hasattr(state, 'note_degree') and random.random() < 0.3:
            state.note_degree = max(1, min(7, state.note_degree + random.randint(-1, 1)))
        
        return state
    
    def _rhythm_mutation(self, state: MelodyState) -> MelodyState:
        """节奏变异"""
        # 可用时值列表
        valid_durations = [0.125, 0.25, 0.5, 1.0, 2.0]  # 1/8, 1/4, 1/2, 1/1, 2/1
        
        if random.random() < 0.4:  # 40%概率变异时值
            state.duration = random.choice(valid_durations)
        
        if random.random() < 0.3:  # 30%概率变异节拍强度
            from .melody import MelodyState
            if not hasattr(state, 'beat_strength'):
                setattr(state, 'beat_strength', 0.8)
            state.beat_strength = max(0, min(1, state.beat_strength + random.uniform(-0.3, 0.3)))
        
        if random.random() < 0.2:  # 20%概率变异切分程度
            from .melody import MelodyState
            if not hasattr(state, 'syncopation'):
                setattr(state, 'syncopation', 0.0)
            state.syncopation = max(0, min(1, state.syncopation + random.uniform(-0.5, 0.5)))
        
        return state
    
    def _dynamic_mutation(self, state: MelodyState) -> MelodyState:
        """力度变异"""
        if random.random() < 0.4:  # 40%概率变异力度
            from .melody import MelodyState
            if not hasattr(state, 'velocity'):
                setattr(state, 'velocity', 80)
            state.velocity = max(0, min(127, int(state.velocity + random.randint(-20, 20))))
        
        if random.random() < 0.3:  # 30%概率变异重音程度
            from .melody import MelodyState
            if not hasattr(state, 'accent'):
                setattr(state, 'accent', 1.0)
            state.accent = max(0, min(1, state.accent + random.uniform(-0.3, 0.3)))
        
        return state
    
    def _structure_mutation(self, state: MelodyState, position: float) -> MelodyState:
        """结构变异"""
        # 结构变异影响较大，降低变异强度
        
        # 段落类型变异
        if random.random() < 0.3:
            from .melody import MelodyState
            if not hasattr(state, 'section_type'):
                setattr(state, 'section_type', 'verse')
            sections = ['verse', 'chorus', 'bridge', 'prelude', 'outro']
            state.section_type = random.choice(sections)
        
        # 对比程度变异
        if random.random() < 0.2:
            from .melody import MelodyState
            if not hasattr(state, 'contrast_level'):
                setattr(state, 'contrast_level', 0.5)
            state.contrast_level = max(0, min(1, state.contrast_level + random.uniform(-0.4, 0.4)))
        
        # 高潮位置影响（基于全局位置）
        if position > 0.6 and random.random() < 0.2:  # 在后60%的区域有概率增强高潮
            from .melody import MelodyState
            if not hasattr(state, 'climax_intensity'):
                setattr(state, 'climax_intensity', 0.0)
            state.climax_intensity = min(1.0, state.climax_intensity + 0.3)
        
        return state


class GeneticAlgorithmEngine:
    """遗传算法引擎"""
    
    def __init__(self, 
                 population_size: int = 50,
                 generations: int = 100,
                 elite_ratio: float = 0.1,
                 mutation_rate: float = 0.1,
                 selection_type: SelectionType = SelectionType.TOURNAMENT,
                 crossover_type: CrossoverType = CrossoverType.SINGLE_POINT):
        
        self.population_size = population_size
        self.generations = generations
        self.elite_ratio = elite_ratio
        self.mutation_rate = mutation_rate
        
        # 初始化操作器
        self.selection_operator = SelectionOperator(selection_type)
        self.crossover_operator = CrossoverOperator(crossover_type)
        self.mutation_operator = MutationOperator(mutation_rate)
        
        # 进化历史记录
        self.generation_history = []
    
    def initialize_population(self, config: MelodyConfig, 
                             melody_generator: Optional[Callable] = None) -> List[MelodyIndividual]:
        """初始化种群"""
        population = []
        
        for _ in range(self.population_size):
            if melody_generator:
                # 使用提供的旋律生成器生成初始个体
                melody_states = melody_generator(config)
            else:
                # 使用默认的随机旋律生成
                melody_states = self._generate_random_melody(config)
            
            individual = MelodyIndividual(
                melody_states=melody_states,
                generation=0
            )
            population.append(individual)
        
        return population
    
    def _generate_random_melody(self, config: MelodyConfig) -> List[MelodyState]:
        """生成随机旋律作为初始个体"""
        from .melody import MelodyState
        
        states = []
        
        for i in range(config.length):
            # 随机生成音符状态
            state = MelodyState(
                note=config.start_note,
                octave=config.start_octave,
                duration=random.choice([0.125, 0.25, 0.5, 1.0]),
                velocity=80,
                time_position=i * 0.25
            )
            
            states.append(state)
        
        return states
    
    def evolve_population(self, population: List[MelodyIndividual], 
                         evaluator: MelodyFitnessEvaluator,
                         config: MelodyConfig) -> List[MelodyIndividual]:
        """进化一代"""
        new_population = []
        
        # 评估当前种群
        for individual in population:
            if individual.fitness == 0.0:
                individual.fitness = individual.calculate_fitness(evaluator)
        
        # 精英保留
        elite_count = int(self.population_size * self.elite_ratio)
        elite = sorted(population, key=lambda ind: ind.fitness, reverse=True)[:elite_count]
        new_population.extend(elite)
        
        # 生成新一代
        while len(new_population) < self.population_size:
            # 选择父代
            parent1 = self.selection_operator.select(population)
            parent2 = self.selection_operator.select(population)
            
            # 交叉
            child1, child2 = self.crossover_operator.crossover(parent1, parent2)
            
            # 变异
            child1 = self.mutation_operator.mutate(child1)
            child2 = self.mutation_operator.mutate(child2)
            
            # 评估子代适应度
            child1.fitness = child1.calculate_fitness(evaluator)
            child2.fitness = child2.calculate_fitness(evaluator)
            
            new_population.extend([child1, child2])
        
        # 确保种群大小正确
        new_population = new_population[:self.population_size]
        
        # 记录这一代的统计信息
        self._record_generation_stats(new_population)
        
        return new_population
    
    def run_evolution(self, config: MelodyConfig, 
                     evaluator: MelodyFitnessEvaluator,
                     melody_generator: Optional[Callable] = None) -> MelodyIndividual:
        """运行完整的进化过程"""
        print(f"开始遗传算法进化: 种群大小={self.population_size}, 代数={self.generations}")
        
        # 初始化种群
        population = self.initialize_population(config, melody_generator)
        
        # 进化循环
        for generation in range(self.generations):
            # 进化一代
            population = self.evolve_population(population, evaluator, config)
            
            # 显示进度
            best_fitness = max(ind.fitness for ind in population)
            avg_fitness = sum(ind.fitness for ind in population) / len(population)
            
            if generation % 10 == 0 or generation == self.generations - 1:
                print(f"第 {generation} 代: 最佳适应度={best_fitness:.2f}, 平均适应度={avg_fitness:.2f}")
            
            # 检查收敛
            if self._check_convergence(population):
                print(f"在第 {generation} 代收敛，提前结束进化")
                break
        
        # 返回最优个体
        best_individual = max(population, key=lambda ind: ind.fitness)
        print(f"进化完成! 最终最佳适应度: {best_individual.fitness:.2f}")
        
        return best_individual
    
    def _record_generation_stats(self, population: List[MelodyIndividual]):
        """记录代数统计信息"""
        if population:
            stats = {
                'generation': len(self.generation_history),
                'best_fitness': max(ind.fitness for ind in population),
                'avg_fitness': sum(ind.fitness for ind in population) / len(population),
                'worst_fitness': min(ind.fitness for ind in population),
                'diversity': self._calculate_diversity(population)
            }
            self.generation_history.append(stats)
    
    def _calculate_diversity(self, population: List[MelodyIndividual]) -> float:
        """计算种群多样性"""
        if len(population) < 2:
            return 1.0
        
        # 基于适应度的多样性计算
        fitness_values = [ind.fitness for ind in population]
        mean_fitness = sum(fitness_values) / len(fitness_values)
        variance = sum((f - mean_fitness) ** 2 for f in fitness_values) / len(fitness_values)
        
        # 标准化多样性分数 (0-1)
        diversity = min(1.0, variance / 1000.0)  # 假设方差最大为1000
        return diversity
    
    def _check_convergence(self, population: List[MelodyIndividual], 
                          tolerance: float = 0.001) -> bool:
        """检查种群是否收敛"""
        if len(self.generation_history) < 5:
            return False
        
        # 检查最近5代的适应度变化
        recent_fitness = [stats['best_fitness'] for stats in self.generation_history[-5:]]
        
        # 如果最近5代适应度变化小于阈值，认为收敛
        max_diff = max(recent_fitness) - min(recent_fitness)
        return max_diff < tolerance
    
    def get_evolution_report(self) -> Dict:
        """获取进化报告"""
        if not self.generation_history:
            return {}
        
        best_fitness_ever = max(stats['best_fitness'] for stats in self.generation_history)
        avg_fitness_final = self.generation_history[-1]['avg_fitness']
        generations_run = len(self.generation_history)
        
        return {
            'total_generations': generations_run,
            'best_fitness_ever': best_fitness_ever,
            'avg_fitness_final': avg_fitness_final,
            'elite_ratio': self.elite_ratio,
            'mutation_rate': self.mutation_rate,
            'population_size': self.population_size,
            'convergence_achieved': generations_run < self.generations
        }
    
    def save_evolution_data(self, filename: str):
        """保存进化数据"""
        import json
        
        data = {
            'evolution_history': self.generation_history,
            'parameters': {
                'population_size': self.population_size,
                'generations': self.generations,
                'elite_ratio': self.elite_ratio,
                'mutation_rate': self.mutation_rate
            },
            'report': self.get_evolution_report()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)