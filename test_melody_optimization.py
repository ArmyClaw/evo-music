#!/usr/bin/env python3
"""
测试旋律连贯性优化功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evo_music.melody import generate_melody, EmotionType
from evo_music.scales import ScaleFactory, ScaleType
from evo_music.notes import NoteName
from evo_music.melody_optimizer import MelodyOptimizer
import json

def test_melody_optimization():
    """测试旋律优化功能"""
    print("=== 测试旋律连贯性优化 ===")
    
    # 测试不同情感的旋律生成
    emotions = ["happy", "sad", "mysterious", "epic"]
    
    for emotion in emotions:
        print(f"\n🎵 测试 {emotion} 情感旋律:")
        
        # 生成原始旋律
        original_melody = generate_melody(emotion=emotion, length=16, enable_optimization=False)
        print(f"原始旋律长度: {len(original_melody)}")
        
        # 生成优化后的旋律
        optimized_melody = generate_melody(emotion=emotion, length=16, enable_optimization=True)
        print(f"优化后旋律长度: {len(optimized_melody)}")
        
        # 分析优化效果
        original_intervals = []
        optimized_intervals = []
        
        for i in range(1, len(original_melody)):
            original_intervals.append(abs(original_melody[i].note.value - original_melody[i-1].note.value))
            
        for i in range(1, len(optimized_melody)):
            optimized_intervals.append(abs(optimized_melody[i].note.value - optimized_melody[i-1].note.value))
        
        avg_original = sum(original_intervals) / len(original_intervals) if original_intervals else 0
        avg_optimized = sum(optimized_intervals) / len(optimized_intervals) if optimized_intervals else 0
        
        print(f"平均音程距离 - 原始: {avg_original:.2f}, 优化后: {avg_optimized:.2f}")
        
        # 检查是否有大跳
        large_jumps_original = sum(1 for x in original_intervals if x > 7)
        large_jumps_optimized = sum(1 for x in optimized_intervals if x > 7)
        
        print(f"大跳次数 (>7) - 原始: {large_jumps_original}, 优化后: {large_jumps_optimized}")

def test_melody_optimizer_directly():
    """直接测试旋律优化器"""
    print("\n=== 直接测试旋律优化器 ===")
    
    # 创建C大调音阶
    scale = ScaleFactory.create_scale(NoteName.C, ScaleType.MAJOR)
    
    # 创建优化器
    optimizer = MelodyOptimizer(scale, max_leap=5)
    
    # 生成一些测试旋律
    test_melody = generate_melody("happy", length=12, enable_optimization=False)
    
    print(f"测试旋律长度: {len(test_melody)}")
    
    # 分析优化前
    intervals = []
    for i in range(1, len(test_melody)):
        interval = abs(test_melody[i].note.value - test_melody[i-1].note.value)
        intervals.append(interval)
        print(f"步骤 {i}: 音程 {interval}")
    
    large_jumps_before = sum(1 for x in intervals if x > 5)
    print(f"优化前大跳次数 (>5): {large_jumps_before}")
    
    # 应用优化
    optimized_melody = optimizer.optimize_sequence(test_melody)
    
    # 分析优化后
    optimized_intervals = []
    for i in range(1, len(optimized_melody)):
        interval = abs(optimized_melody[i].note.value - optimized_melody[i-1].note.value)
        optimized_intervals.append(interval)
        print(f"优化后步骤 {i}: 音程 {interval}")
    
    large_jumps_after = sum(1 for x in optimized_intervals if x > 5)
    print(f"优化后大跳次数 (>5): {large_jumps_after}")
    
    if large_jumps_after < large_jumps_before:
        print("✅ 优化成功：减少了不协和跳跃")
    else:
        print("⚠️ 优化效果不明显")

def test_harmony_optimization():
    """测试和声优化功能"""
    print("\n=== 测试和声优化 ===")
    
    # 生成原始旋律
    original_melody = generate_melody("happy", length=8, enable_optimization=False)
    
    # 应用和声优化
    from evo_music.melody_optimizer import HarmonyOptimizer
    scale = ScaleFactory.create_scale(NoteName.C, ScaleType.MAJOR)
    harmony_optimizer = HarmonyOptimizer(scale)
    
    # 简单的I-IV-V和弦进行
    chord_progression = [0, 5, 7, 0]  # C-F-G-C
    
    # 检查和谐度
    harmony_scores = harmony_optimizer.check_harmony(original_melody, chord_progression)
    print(f"原始旋律和谐度: {harmony_scores}")
    
    # 应用和声优化
    optimized_melody = harmony_optimizer.optimize_for_harmony(original_melody, chord_progression)
    
    # 检查优化后和谐度
    optimized_scores = harmony_optimizer.check_harmony(optimized_melody, chord_progression)
    print(f"优化后旋律和谐度: {optimized_scores}")

if __name__ == "__main__":
    test_melody_optimization()
    test_melody_optimizer_directly()
    test_harmony_optimization()
    print("\n=== 测试完成 ===")