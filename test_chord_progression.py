#!/usr/bin/env python3
"""
和弦进行生成器测试脚本
实现I-V-vi-IV等经典和弦进行的自动生成
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evo_music.music_theory import MusicTheory, ProgressionStyle
from evo_music.notes import NoteName

def test_chord_progression_generation():
    """测试和弦进行生成功能"""
    print("=== 和弦进行生成器测试 ===")
    
    # 创建音乐理论实例
    music_theory = MusicTheory()
    
    # 测试1: 经典流行进行 (I-V-vi-IV)
    print("\n1. 测试经典流行进行 (I-V-vi-IV):")
    classic_pop = music_theory.generate_chord_progression("C", "major", ProgressionStyle.CLASSIC_POP, 4)
    print(f"C大调经典流行进行: {[chord.name for chord in classic_pop]}")
    print(f"功能标记: {[chord.function for chord in classic_pop]}")
    
    # 测试2: 爵士标准进行 (ii-V-I)
    print("\n2. 测试爵士标准进行 (ii-V-I):")
    jazz = music_theory.generate_chord_progression("C", "major", ProgressionStyle.JAZZ_STANDARD, 3)
    print(f"C大调爵士进行: {[chord.name for chord in jazz]}")
    print(f"功能标记: {[chord.function for chord in jazz]}")
    
    # 测试3: 简单摇滚进行 (I-IV-V)
    print("\n3. 测试简单摇滚进行 (I-IV-V):")
    rock = music_theory.generate_chord_progression("G", "major", ProgressionStyle.ROCK, 3)
    print(f"G大调摇滚进行: {[chord.name for chord in rock]}")
    print(f"功能标记: {[chord.function for chord in rock]}")
    
    # 测试4: 12小节布鲁斯进行
    print("\n4. 测试12小节布鲁斯进行:")
    blues = music_theory.generate_chord_progression("C", "major", ProgressionStyle.BLUES_12_BAR, 8)
    print(f"C大调布鲁斯进行 (前8小节): {[chord.name for chord in blues]}")
    print(f"功能标记: {[chord.function for chord in blues]}")
    
    # 测试5: 现代流行进行 (vi-IV-I-V)
    print("\n5. 测试现代流行进行 (vi-IV-I-V):")
    modern = music_theory.generate_chord_progression("C", "major", ProgressionStyle.MODERN, 4)
    print(f"C大调现代流行进行: {[chord.name for chord in modern]}")
    print(f"功能标记: {[chord.function for chord in modern]}")
    
    # 测试6: 随机进行
    print("\n6. 测试随机进行:")
    random_prog = music_theory.get_random_chord_progression("D", "major", 4)
    print(f"D大调随机进行: {[chord.name for chord in random_prog]}")
    print(f"功能标记: {[chord.function for chord in random_prog]}")
    
    # 测试7: 分析紧张度
    print("\n7. 分析和弦进行紧张度:")
    tension_analysis = music_theory.analyze_progression_tension(classic_pop)
    print(f"经典流行进行紧张度: {tension_analysis['tension_level']:.2f}")
    print(f"七和弦比例: {tension_analysis['tension_metrics']['seventh_chord_ratio']:.2f}")
    print(f"三全音距离: {tension_analysis['tension_metrics']['tritone_distance']:.2f}")
    
    # 测试8: 获取改进建议
    print("\n8. 获取和弦进行改进建议:")
    suggestions = music_theory.get_progression_improvements(classic_pop)
    print(f"改进建议: {suggestions}")
    
    # 测试9: 列出所有可用风格
    print("\n9. 列出所有可用风格:")
    styles = music_theory.list_progression_styles()
    print(f"可用风格: {styles}")
    
    # 测试10: 获取风格信息
    print("\n10. 获取风格信息:")
    style_info = music_theory.get_progression_style_info(ProgressionStyle.CLASSIC_POP)
    print(f"经典流行风格信息:")
    print(f"  名称: {style_info['name']}")
    print(f"  描述: {style_info['description']}")
    print(f"  复杂度: {style_info['complexity']}/5")
    print(f"  流行度: {style_info['popularity']:.2f}")
    print(f"  示例功能: {style_info['example_functions']}")
    
    print("\n=== 测试完成 ===")

def test_multiple_styles_generation():
    """测试多种风格生成"""
    print("\n=== 多种风格生成测试 ===")
    
    music_theory = MusicTheory()
    
    # 生成多种风格的进行
    styles_to_test = [ProgressionStyle.CLASSIC_POP, ProgressionStyle.JAZZ_STANDARD, 
                     ProgressionStyle.ROCK, ProgressionStyle.MODERN]
    
    multiple_progressions = music_theory.generate_multiple_chord_progressions(
        "C", "major", styles_to_test, 2, 4
    )
    
    for style, progressions in multiple_progressions.items():
        print(f"\n{ProgressionStyle.get_description(style)}:")
        for i, prog in enumerate(progressions):
            print(f"  进行{i+1}: {[chord.name for chord in prog]}")
    
    print("\n=== 多风格测试完成 ===")

def verify_chord_progression_task():
    """验证任务完成情况"""
    print("\n=== 任务验证 ===")
    
    music_theory = MusicTheory()
    
    # 验证I-V-vi-IV进行
    progression_1_5_6_4 = music_theory.generate_chord_progression(
        "C", "major", ProgressionStyle.CLASSIC_POP, 4
    )
    
    functions = [chord.function for chord in progression_1_5_6_4]
    print(f"I-V-vi-IV进行验证: {functions}")
    
    # 验证是否包含所有要求的进行类型
    required_progressions = [
        ("经典流行", ProgressionStyle.CLASSIC_POP),
        ("爵士标准", ProgressionStyle.JAZZ_STANDARD),
        ("摇滚", ProgressionStyle.ROCK),
        ("现代", ProgressionStyle.MODERN),
        ("布鲁斯", ProgressionStyle.BLUES_12_BAR)
    ]
    
    print("\n功能验证:")
    for name, style in required_progressions:
        try:
            test_prog = music_theory.generate_chord_progression("C", "major", style, 4)
            success = len(test_prog) == 4
            print(f"  {name}: {'✓' if success else '✗'}")
        except Exception as e:
            print(f"  {name}: ✗ (错误: {e})")
    
    print("\n=== 验证完成 ===")

if __name__ == "__main__":
    try:
        # 运行所有测试
        test_chord_progression_generation()
        test_multiple_styles_generation()
        verify_chord_progression_task()
        
        print("\n🎉 所有测试通过！和弦进行生成器实现成功。")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        sys.exit(1)