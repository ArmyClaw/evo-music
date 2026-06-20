#!/usr/bin/env python3
"""
进化迭代引擎 - 实现多代进化，收敛到高分旋律
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Optional, Callable
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from evo_music.genetic_algorithm import (
    GeneticAlgorithmEngine, MelodyIndividual, SelectionType, CrossoverType
)
from evo_music.melody import MelodyConfig, EmotionType, MelodyState
from evo_music.fitness import MelodyFitnessEvaluator
from evo_music.scales import ScaleType, ScaleFactory
from evo_music.notes import NoteName


class EvolutionIterationEngine:
    """进化迭代引擎 - 专门实现多代进化收敛功能"""
    
    def __init__(self, 
                 population_size: int = 50,
                 generations: int = 100,
                 elite_ratio: float = 0.1,
                 mutation_rate: float = 0.1,
                 convergence_threshold: float = 0.001,
                 stagnation_generations: int = 20):
        
        self.population_size = population_size
        self.generations = generations
        self.elite_ratio = elite_ratio
        self.mutation_rate = mutation_rate
        self.convergence_threshold = convergence_threshold
        self.stagnation_generations = stagnation_generations
        
        # 初始化遗传算法引擎
        self.ga_engine = GeneticAlgorithmEngine(
            population_size=population_size,
            generations=generations,
            elite_ratio=elite_ratio,
            mutation_rate=mutation_rate,
            selection_type=SelectionType.TOURNAMENT,
            crossover_type=CrossoverType.SINGLE_POINT
        )
        
        # 进化历史和统计
        self.evolution_history = []
        self.best_individual_ever = None
        self.best_fitness_ever = 0.0
        
    def create_initial_population(self, config: MelodyConfig, 
                                melody_generator: Optional[Callable] = None) -> List[MelodyIndividual]:
        """创建初始种群"""
        print(f"创建初始种群: {self.population_size} 个个体")
        
        population = []
        for i in range(self.population_size):
            if melody_generator:
                melody_states = melody_generator(config)
            else:
                melody_states = self._generate_diverse_melody(config, i)
            
            individual = MelodyIndividual(
                melody_states=melody_states,
                generation=0,
                parent_ids=(0, 0)
            )
            population.append(individual)
        
        return population
    
    def _generate_diverse_melody(self, config: MelodyConfig, seed: int) -> List[MelodyState]:
        """生成多样化的初始旋律"""
        random.seed(seed)
        states = []
        
        # 基于情感类型生成不同特征的旋律
        if config.emotion == EmotionType.HAPPY:
            # 快速、明亮的旋律
            base_duration = 0.25
            base_velocity = 90
            base_octave = 4
        elif config.emotion == EmotionType.SAD:
            # 缓慢、柔和的旋律
            base_duration = 0.5
            base_velocity = 60
            base_octave = 3
        elif config.emotion == EmotionType.MYSTERIOUS:
            # 不规则、神秘的旋律
            base_duration = random.choice([0.125, 0.25, 0.5])
            base_velocity = random.randint(50, 80)
            base_octave = random.randint(3, 5)
        else:
            # 中性旋律
            base_duration = 0.25
            base_velocity = 80
            base_octave = 4
        
        for i in range(config.length):
            # 在音阶内选择音符
            scale_notes = config.scale.get_notes()
            note = random.choice(scale_notes)
            
            # 添加一些音程变化
            if i > 0 and random.random() < 0.3:
                # 30%概率与前一个音符保持音程关系
                prev_note = states[-1].note
                interval = random.choice([-2, -1, 1, 2])  # 小音程跳跃
                note_index = scale_notes.index(prev_note)
                note_index = max(0, min(len(scale_notes) - 1, note_index + interval))
                note = scale_notes[note_index]
            
            # 创建旋律状态
            state = MelodyState(
                note=note,
                octave=base_octave + random.randint(-1, 1),
                duration=base_duration * random.choice([0.5, 1.0, 1.5, 2.0]),
                velocity=base_velocity + random.randint(-20, 20),
                time_position=i * 0.25
            )
            
            states.append(state)
        
        return states
    
    def run_evolution_iteration(self, config: MelodyConfig,
                              melody_generator: Optional[Callable] = None) -> MelodyIndividual:
        """运行完整的进化迭代"""
        print("=" * 60)
        print("开始进化迭代")
        print("=" * 60)
        
        # 创建评估器
        evaluator = MelodyFitnessEvaluator(config.scale)
        
        # 创建初始种群
        population = self.create_initial_population(config, melody_generator)
        
        # 评估初始种群
        for individual in population:
            individual.fitness = individual.calculate_fitness(evaluator)
        
        # 初始化最佳个体
        self.best_individual_ever = max(population, key=lambda ind: ind.fitness)
        self.best_fitness_ever = self.best_individual_ever.fitness
        
        print(f"初始最佳适应度: {self.best_fitness_ever:.4f}")
        
        # 进化主循环
        stagnation_counter = 0
        last_best_fitness = self.best_fitness_ever
        
        for generation in range(self.generations):
            # 进化一代
            population = self.ga_engine.evolve_population(population, evaluator, config)
            
            # 更新最佳个体
            current_best = max(population, key=lambda ind: ind.fitness)
            if current_best.fitness > self.best_fitness_ever:
                self.best_individual_ever = current_best
                self.best_fitness_ever = current_best.fitness
                stagnation_counter = 0
            else:
                stagnation_counter += 1
            
            # 计算统计信息
            best_fitness = current_best.fitness
            avg_fitness = sum(ind.fitness for ind in population) / len(population)
            diversity = self.ga_engine._calculate_diversity(population)
            
            # 记录进化历史
            generation_stats = {
                'generation': generation,
                'best_fitness': best_fitness,
                'avg_fitness': avg_fitness,
                'diversity': diversity,
                'best_fitness_ever': self.best_fitness_ever,
                'stagnation_counter': stagnation_counter
            }
            self.evolution_history.append(generation_stats)
            
            # 显示进度
            if generation % 10 == 0 or generation == self.generations - 1:
                print(f"第 {generation:3d} 代: "
                      f"最佳={best_fitness:.4f}, "
                      f"平均={avg_fitness:.4f}, "
                      f"多样={diversity:.4f}, "
                      f"停滞={stagnation_counter}")
            
            # 检查收敛条件
            if self._check_convergence(generation_stats):
                print(f"\n在第 {generation} 代达到收敛条件，进化结束")
                break
            
            # 检查停滞
            if stagnation_counter >= self.stagnation_generations:
                print(f"\n连续 {stagnation_counter} 代未改进，进化结束")
                break
        
        print("=" * 60)
        print("进化迭代完成")
        print("=" * 60)
        
        # 显示最终结果
        self._display_final_results()
        
        # 保存进化数据
        self._save_evolution_data(config)
        
        return self.best_individual_ever
    
    def _check_convergence(self, stats: Dict) -> bool:
        """检查是否收敛"""
        # 1. 适应度变化小于阈值
        if len(self.evolution_history) > 10:
            recent_best = [h['best_fitness'] for h in self.evolution_history[-10:]]
            fitness_change = max(recent_best) - min(recent_best)
            if fitness_change < self.convergence_threshold:
                return True
        
        # 2. 多样性过低（种群趋于同质）- 使用更合理的阈值
        if stats['diversity'] < 0.02:  # 从0.05调整为更合理的值
            print(f"种群多样性过低: {stats['diversity']:.4f}")
            return True
        
        # 3. 达到理论上的高适应度
        if stats['best_fitness'] > 0.95:  # 95分认为接近完美
            print(f"达到高适应度阈值: {stats['best_fitness']:.4f}")
            return True
        
        return False
    
    def _display_final_results(self):
        """显示最终结果"""
        if not self.evolution_history:
            return
        
        final_stats = self.evolution_history[-1]
        
        print(f"\n🎯 最终结果:")
        print(f"   最佳适应度: {self.best_fitness_ever:.4f}")
        print(f"   进化代数: {len(self.evolution_history)}")
        print(f"   最终平均适应度: {final_stats['avg_fitness']:.4f}")
        print(f"   最终多样性: {final_stats['diversity']:.4f}")
        
        # 进化效率分析
        if len(self.evolution_history) > 1:
            improvement = self.best_fitness_ever - self.evolution_history[0]['best_fitness']
            improvement_rate = improvement / len(self.evolution_history)
            print(f"   进化效率: {improvement:.4f} / {len(self.evolution_history)} = {improvement_rate:.6f} 每代")
        
        # 收敛状态
        converged = final_stats['stagnation_counter'] >= self.stagnation_generations
        print(f"   收敛状态: {'已收敛' if converged else '未完全收敛'}")
    
    def _save_evolution_data(self, config: MelodyConfig):
        """保存进化数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evolution_iteration_{timestamp}.json"
        
        data = {
            'timestamp': timestamp,
            'config': {
                'population_size': self.population_size,
                'generations': self.generations,
                'elite_ratio': self.elite_ratio,
                'mutation_rate': self.mutation_rate,
                'convergence_threshold': self.convergence_threshold,
                'stagnation_generations': self.stagnation_generations,
                'emotion': config.emotion.value if config.emotion else None,
                'scale_type': config.scale.scale_type if config.scale else None,
                'length': config.length
            },
            'evolution_history': self.evolution_history,
            'results': {
                'best_fitness_ever': self.best_fitness_ever,
                'total_generations': len(self.evolution_history),
                'converged': self.evolution_history[-1]['stagnation_counter'] >= self.stagnation_generations if self.evolution_history else False
            },
            'best_individual_genes': self.best_individual_ever.get_gene_info() if self.best_individual_ever else None
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"进化数据已保存到: {filename}")
    
    def get_evolution_summary(self) -> Dict:
        """获取进化摘要"""
        if not self.evolution_history:
            return {}
        
        return {
            'total_generations': len(self.evolution_history),
            'best_fitness_ever': self.best_fitness_ever,
            'avg_fitness_final': self.evolution_history[-1]['avg_fitness'],
            'diversity_final': self.evolution_history[-1]['diversity'],
            'convergence_achieved': self.evolution_history[-1]['stagnation_counter'] >= self.stagnation_generations,
            'evolution_efficiency': self._calculate_evolution_efficiency()
        }
    
    def _calculate_evolution_efficiency(self) -> float:
        """计算进化效率"""
        if len(self.evolution_history) < 2:
            return 0.0
        
        total_improvement = self.best_fitness_ever - self.evolution_history[0]['best_fitness']
        return total_improvement / len(self.evolution_history)


def run_multi_scenario_evolution():
    """运行多场景进化测试"""
    print("🧪 多场景进化迭代测试")
    print("=" * 60)
    
    # 不同情感的配置
    scenarios = [
        {
            'name': '快乐情感',
            'emotion': EmotionType.HAPPY,
            'length': 32,
            'population_size': 40,
            'generations': 50
        },
        {
            'name': '悲伤情感', 
            'emotion': EmotionType.SAD,
            'length': 32,
            'population_size': 40,
            'generations': 50
        },
        {
            'name': '神秘情感',
            'emotion': EmotionType.MYSTERIOUS,
            'length': 32,
            'population_size': 40,
            'generations': 50
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(scenarios):
        print(f"\n🎵 场景 {i+1}: {scenario['name']}")
        print("-" * 40)
        
        # 创建配置
        config = MelodyConfig(
            scale=ScaleFactory.create_scale(NoteName.C, "major"),
            emotion=scenario['emotion'],
            length=scenario['length']
        )
        
        # 创建进化引擎
        engine = EvolutionIterationEngine(
            population_size=scenario['population_size'],
            generations=scenario['generations'],
            elite_ratio=0.1,
            mutation_rate=0.1
        )
        
        # 运行进化
        start_time = time.time()
        best_individual = engine.run_evolution_iteration(config)
        end_time = time.time()
        
        # 记录结果
        result = {
            'scenario': scenario['name'],
            'best_fitness': best_individual.fitness,
            'total_generations': len(engine.evolution_history),
            'time_elapsed': end_time - start_time,
            'summary': engine.get_evolution_summary()
        }
        results.append(result)
        
        # 比较结果
        print(f"完成耗时: {end_time - start_time:.2f} 秒")
    
    # 显示比较结果
    print("\n📊 场景比较结果")
    print("=" * 60)
    for result in results:
        print(f"{result['scenario']}:")
        print(f"  最佳适应度: {result['best_fitness']:.4f}")
        print(f"  进化代数: {result['total_generations']}")
        print(f"  耗时: {result['time_elapsed']:.2f} 秒")
        print(f"  效率: {result['summary']['evolution_efficiency']:.6f} 每代")
        print()


def run_convergence_test():
    """运行收敛性测试"""
    print("🎯 收敛性测试")
    print("=" * 60)
    
    # 创建配置
    config = MelodyConfig(
        scale=ScaleFactory.create_scale(NoteName.C, "major"),
        emotion=EmotionType.HAPPY,
        length=64  # 较长的旋律
    )
    
    # 创建进化引擎（设置较低的收敛阈值）
    engine = EvolutionIterationEngine(
        population_size=50,
        generations=100,
        elite_ratio=0.1,
        mutation_rate=0.05,
        convergence_threshold=0.0001,
        stagnation_generations=30
    )
    
    # 运行进化
    best_individual = engine.run_evolution_iteration(config)
    
    # 分析收敛过程
    print(f"\n📈 收敛分析:")
    print(f"  最终最佳适应度: {best_individual.fitness:.4f}")
    print(f"  进化代数: {len(engine.evolution_history)}")
    
    # 绘制收敛曲线（简化版）
    print(f"  收敛曲线:")
    for i in range(0, len(engine.evolution_history), max(1, len(engine.evolution_history)//10)):
        stats = engine.evolution_history[i]
        print(f"    第 {stats['generation']:3d} 代: {stats['best_fitness']:.4f}")


if __name__ == "__main__":
    import argparse
    
    print("🧬 进化迭代引擎")
    print("=" * 60)
    
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='进化迭代引擎')
    parser.add_argument('--mode', type=str, choices=['1', '2', '3'], default='1',
                        help='运行模式: 1=单场景, 2=多场景, 3=收敛测试')
    parser.add_argument('--headless', action='store_true', 
                        help='无头模式，不等待用户输入')
    args = parser.parse_args()
    
    if args.mode == "1" or (not args.headless and not hasattr(args, 'mode')):
        # 单场景进化
        print("🎵 运行单场景进化")
        config = MelodyConfig(
            scale=ScaleFactory.create_scale(NoteName.C, "major"),
            emotion=EmotionType.HAPPY,
            length=32
        )
        
        engine = EvolutionIterationEngine(
            population_size=30,
            generations=50,
            elite_ratio=0.1,
            mutation_rate=0.1
        )
        
        best_individual = engine.run_evolution_iteration(config)
        
    elif args.mode == "2":
        # 多场景测试
        print("🧪 运行多场景测试")
        run_multi_scenario_evolution()
        
    elif args.mode == "3":
        # 收敛性测试
        print("🎯 运行收敛性测试")
        run_convergence_test()