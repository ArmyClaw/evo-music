#!/usr/bin/env python3
"""
遗传算法演示 - 展示选择/交叉/变异/精英保留功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from evo_music.genetic_algorithm import (
    GeneticAlgorithmEngine, MelodyIndividual, SelectionType, CrossoverType
)
from evo_music.melody import MelodyConfig, EmotionType, MelodyState
from evo_music.fitness import MelodyFitnessEvaluator
from evo_music.scales import ScaleType, ScaleFactory
from evo_music.notes import NoteName


def create_random_individual(length: int = 16) -> MelodyIndividual:
    """创建随机个体用于演示"""
    states = []
    for i in range(length):
        state = MelodyState(
            note=NoteName.C,
            octave=4,
            duration=0.25,
            velocity=80,
            time_position=i * 0.25
        )
        states.append(state)
    
    return MelodyIndividual(melody_states=states, generation=0)


def test_selection_operators():
    """测试选择操作"""
    print("=== 测试选择操作 ===")
    
    # 创建测试种群
    population = [create_random_individual() for _ in range(10)]
    for i, ind in enumerate(population):
        ind.fitness = i * 10  # 设置不同的适应度
    
    # 测试锦标赛选择
    selector = GeneticAlgorithmEngine(population_size=20, generations=5)
    tournament_selector = selector.selection_operator
    
    print("锦标赛选择结果:")
    selected = tournament_selector.select(population)
    print(f"选中个体适应度: {selected.fitness}")
    
    # 测试轮盘赌选择
    selector.selection_type = SelectionType.ROULETTE_WHEEL
    selected = selector.selection_operator.select(population)
    print(f"轮盘赌选择适应度: {selected.fitness}")
    
    # 测试精英选择
    selector.selection_type = SelectionType.ELITE
    selected = selector.selection_operator.select(population)
    print(f"精英选择适应度: {selected.fitness}")


def test_crossover_operators():
    """测试交叉操作"""
    print("\n=== 测试交叉操作 ===")
    
    # 创建父代
    parent1 = create_random_individual(8)
    parent2 = create_random_individual(8)
    
    parent1.fitness = 80
    parent2.fitness = 60
    
    print("父代1适应度:", parent1.fitness)
    print("父代2适应度:", parent2.fitness)
    
    # 测试单点交叉
    engine = GeneticAlgorithmEngine(population_size=20, generations=5)
    child1, child2 = engine.crossover_operator.crossover(parent1, parent2)
    
    print("单点交叉 - 子代1适应度:", child1.fitness)
    print("单点交叉 - 子代2适应度:", child2.fitness)
    
    # 测试均匀交叉
    engine.crossover_type = CrossoverType.UNIFORM
    child1, child2 = engine.crossover_operator.crossover(parent1, parent2)
    
    print("均匀交叉 - 子代1适应度:", child1.fitness)
    print("均匀交叉 - 子代2适应度:", child2.fitness)
    
    # 测试混合交叉
    engine.crossover_type = CrossoverType.BLEND
    child1, child2 = engine.crossover_operator.crossover(parent1, parent2)
    
    print("混合交叉 - 子代1适应度:", child1.fitness)
    print("混合交叉 - 子代2适应度:", child2.fitness)


def test_mutation():
    """测试变异操作"""
    print("\n=== 测试变异操作 ===")
    
    # 创建原始个体
    original = create_random_individual(8)
    original.fitness = 70
    print("原始个体适应度:", original.fitness)
    
    # 创建引擎并设置高变异率以便观察
    engine = GeneticAlgorithmEngine(population_size=20, generations=5, mutation_rate=0.5)
    
    # 变异
    mutated = engine.mutation_operator.mutate(original)
    print("变异后适应度:", mutated.fitness)
    
    # 显示基因信息变化
    print("\n原始个体基因信息:")
    original_genes = original.get_gene_info()
    print(f"音高基因数量: {len(original_genes.get('pitch_genes', []))}")
    
    print("变异后个体基因信息:")
    mutated_genes = mutated.get_gene_info()
    print(f"音高基因数量: {len(mutated_genes.get('pitch_genes', []))}")


def test_elite_preservation():
    """测试精英保留"""
    print("\n=== 测试精英保留 ===")
    
    # 创建配置
    config = MelodyConfig(
        scale=ScaleFactory.create_scale(NoteName.C, "major"),
        length=16
    )
    
    # 创建种群，其中一些个体有高适应度
    population = [create_random_individual() for _ in range(20)]
    for i in range(len(population)):
        population[i].fitness = 50 + i * 2  # 适应度从50到90
    
    # 创建引擎，设置高精英比例
    engine = GeneticAlgorithmEngine(
        population_size=20, 
        generations=5, 
        elite_ratio=0.2  # 保留20%的精英
    )
    
    # 创建评估器
    evaluator = MelodyFitnessEvaluator(config.scale)
    
    # 模拟一代进化
    new_population = engine.evolve_population(population, evaluator, config)
    
    # 检查精英是否保留
    elite_count = int(engine.population_size * engine.elite_ratio)
    elite_fitness = [ind.fitness for ind in population[:elite_count]]
    
    print("原始精英适应度:", elite_fitness)
    
    # 新种群中的前几个应该是精英
    new_elite_fitness = [ind.fitness for ind in new_population[:elite_count]]
    print("新一代精英适应度:", new_elite_fitness)
    
    # 检查最高适应度是否保持或提高
    max_old = max(ind.fitness for ind in population)
    max_new = max(ind.fitness for ind in new_population)
    print(f"最高适应度: 旧={max_old:.2f}, 新={max_new:.2f}")


def run_full_genetic_demo():
    """运行完整的遗传算法演示"""
    print("\n=== 完整遗传算法演示 ===")
    
    # 创建配置
    config = MelodyConfig(
        scale=ScaleFactory.create_scale(NoteName.C, "major"),
        emotion=EmotionType.HAPPY,
        length=32,
        enable_optimization=True
    )
    
    # 创建评估器
    evaluator = MelodyFitnessEvaluator(config.scale)
    
    # 创建遗传算法引擎
    engine = GeneticAlgorithmEngine(
        population_size=30,
        generations=20,
        elite_ratio=0.1,
        mutation_rate=0.1,
        selection_type=SelectionType.TOURNAMENT,
        crossover_type=CrossoverType.SINGLE_POINT
    )
    
    print("开始进化过程...")
    print(f"参数: 种群大小={engine.population_size}, 代数={engine.generations}")
    
    # 运行进化
    best_individual = engine.run_evolution(config, evaluator)
    
    # 显示结果
    print(f"\n最佳个体适应度: {best_individual.fitness:.2f}")
    print(f"进化代数: {len(engine.generation_history)}")
    
    # 获取进化报告
    report = engine.get_evolution_report()
    print(f"最终平均适应度: {report.get('avg_fitness_final', 0):.2f}")
    print(f"是否收敛: {'是' if report.get('convergence_achieved', False) else '否'}")
    
    # 保存进化数据
    engine.save_evolution_data("genetic_evolution_data.json")
    print("进化数据已保存到 genetic_evolution_data.json")


if __name__ == "__main__":
    print("遗传算法引擎演示")
    print("=" * 50)
    
    # 运行所有测试
    test_selection_operators()
    test_crossover_operators()
    test_mutation()
    test_elite_preservation()
    
    # 运行完整演示
    run_full_genetic_demo()
    
    print("\n演示完成!")