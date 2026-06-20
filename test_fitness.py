"""
测试适应度函数模块
验证音程平滑度、节奏规律性、调性一致性的评分功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'evo_music'))

from evo_music.fitness import MelodyFitnessEvaluator
from evo_music.notes import NoteName
from evo_music.scales import ScaleFactory, ScaleType
from evo_music.melody_optimizer import OptimizedMelodyState

# 导入音阶间隔常量
from evo_music.scales import SCALE_INTERVALS

def create_test_melody():
    """创建测试旋律"""
    # 创建一个简单的旋律序列
    test_melody = [
        OptimizedMelodyState(NoteName.C, 4, 0.5, 80, 0.0),
        OptimizedMelodyState(NoteName.D, 4, 0.5, 80, 0.25),
        OptimizedMelodyState(NoteName.E, 4, 1.0, 80, 0.5),
        OptimizedMelodyState(NoteName.F, 4, 0.5, 80, 1.0),
        OptimizedMelodyState(NoteName.G, 4, 1.0, 80, 1.5),
        OptimizedMelodyState(NoteName.A, 4, 0.5, 80, 2.0),
        OptimizedMelodyState(NoteName.B, 4, 1.0, 80, 2.5),
        OptimizedMelodyState(NoteName.C, 5, 2.0, 80, 3.0),
    ]
    return test_melody

def create_smooth_melody():
    """创建一个平滑的旋律（应该得分高）"""
    smooth_melody = [
        OptimizedMelodyState(NoteName.C, 4, 0.5, 80, 0.0),
        OptimizedMelodyState(NoteName.C, 4, 0.5, 80, 0.25),
        OptimizedMelodyState(NoteName.D, 4, 1.0, 80, 0.5),
        OptimizedMelodyState(NoteName.E, 4, 0.5, 80, 1.0),
        OptimizedMelodyState(NoteName.F, 4, 1.0, 80, 1.5),
        OptimizedMelodyState(NoteName.G, 4, 0.5, 80, 2.0),
        OptimizedMelodyState(NoteName.A, 4, 1.0, 80, 2.5),
        OptimizedMelodyState(NoteName.B, 4, 1.0, 80, 3.0),
        OptimizedMelodyState(NoteName.C, 4, 2.0, 80, 4.0),
    ]
    return smooth_melody

def create_jumpy_melody():
    """创建一个跳跃剧烈的旋律（应该得分低）"""
    jumpy_melody = [
        OptimizedMelodyState(NoteName.C, 4, 0.5, 80, 0.0),
        OptimizedMelodyState(NoteName.G, 5, 0.5, 80, 0.25),  # 大跳
        OptimizedMelodyState(NoteName.C, 3, 1.0, 80, 0.5),   # 大跳向下
        OptimizedMelodyState(NoteName.F, 5, 0.5, 80, 1.0),  # 大跳
        OptimizedMelodyState(NoteName.E, 3, 1.0, 80, 1.5),  # 大跳向下
        OptimizedMelodyState(NoteName.A, 5, 0.5, 80, 2.0),  # 大跳
        OptimizedMelodyState(NoteName.D, 3, 1.0, 80, 2.5),  # 大跳向下
        OptimizedMelodyState(NoteName.B, 5, 2.0, 80, 3.0),  # 大跳
    ]
    return jumpy_melody

def test_fitness_evaluation():
    """测试适应度评估"""
    print("🧪 测试适应度函数模块")
    print("=" * 50)
    
    # 创建C大调音阶
    scale = ScaleFactory.create_scale(NoteName.C, ScaleType.MAJOR)
    evaluator = MelodyFitnessEvaluator(scale)
    
    # 测试不同类型的旋律
    test_melody = create_test_melody()
    smooth_melody = create_smooth_melody()
    jumpy_melody = create_jumpy_melody()
    
    print("\n🎵 测试1: 标准测试旋律")
    score1 = evaluator.evaluate_fitness(test_melody)
    print(f"总分数: {score1.total_score:.1f}")
    print(f"  音程平滑度: {score1.interval_smoothness:.1f}")
    print(f"  节奏规律性: {score1.rhythm_regularity:.1f}")
    print(f"  调性一致性: {score1.tonal_consistency:.1f}")
    
    print("\n🎵 测试2: 平滑旋律")
    score2 = evaluator.evaluate_fitness(smooth_melody)
    print(f"总分数: {score2.total_score:.1f}")
    print(f"  音程平滑度: {score2.interval_smoothness:.1f}")
    print(f"  节奏规律性: {score2.rhythm_regularity:.1f}")
    print(f"  调性一致性: {score2.tonal_consistency:.1f}")
    
    print("\n🎵 测试3: 跳跃剧烈旋律")
    score3 = evaluator.evaluate_fitness(jumpy_melody)
    print(f"总分数: {score3.total_score:.1f}")
    print(f"  音程平滑度: {score3.interval_smoothness:.1f}")
    print(f"  节奏规律性: {score3.rhythm_regularity:.1f}")
    print(f"  调性一致性: {score3.tonal_consistency:.1f}")
    
    print("\n🔍 详细指标 (标准测试旋律):")
    for key, value in score1.detailed_metrics.items():
        print(f"  {key}: {value:.3f}")
    
    print("\n🆚 旋律对比测试:")
    comparison = evaluator.compare_melodies(smooth_melody, jumpy_melody)
    print(f"平滑旋律分数: {comparison['melody1']['total_score']:.1f}")
    print(f"跳跃旋律分数: {comparison['melody2']['total_score']:.1f}")
    print(f"更好的旋律: {comparison['better_melody']}")
    print(f"分数差异: {comparison['score_difference']:.1f}")
    
    # 验证预期结果
    print("\n✅ 测试结果验证:")
    expected_smooth_better = score2.total_score > score3.total_score
    expected_test_reasonable = 40 < score1.total_score < 90
    
    print(f"  平滑旋律分数 > 跳跃旋律分数: {expected_smooth_better} ✓")
    print(f"  测试旋律分数在合理范围内: {expected_test_reasonable} ✓")
    
    if expected_smooth_better and expected_test_reasonable:
        print("\n🎉 所有测试通过！适应度函数运行正常")
        return True
    else:
        print("\n❌ 测试失败，需要检查适应度函数实现")
        return False

if __name__ == "__main__":
    success = test_fitness_evaluation()
    sys.exit(0 if success else 1)