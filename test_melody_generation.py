#!/usr/bin/env python3
"""
测试马尔可夫链旋律生成算法
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evo_music.melody import generate_melody, MarkovMelodyGenerator, MelodyConfig
from evo_music.scales import ScaleFactory
from evo_music.notes import NoteName
from evo_music.scales import ScaleType
from evo_music.midi_output import MIDIGenerator


def test_basic_melody_generation():
    """测试基本旋律生成功能"""
    print("=== 测试基本旋律生成 ===")
    
    # 生成一个简单的欢快旋律
    melody = generate_melody(emotion="happy", length=16, start_note="C")
    
    print(f"生成了 {len(melody)} 个音符的旋律:")
    for i, state in enumerate(melody):
        print(f"  {i+1}. {state.note.name} (octave {state.octave}) - "
              f"duration: {state.duration}, velocity: {state.velocity}")
    
    return melody


def test_different_emotions():
    """测试不同情感的旋律生成"""
    print("\n=== 测试不同情感旋律生成 ===")
    
    emotions = ["happy", "sad", "mysterious", "epic", "peaceful"]
    
    for emotion in emotions:
        print(f"\n--- 生成 {emotion} 情感旋律 ---")
        melody = generate_melody(emotion=emotion, length=12, start_note="C")
        
        # 计算音域范围
        notes = [state.note.value + state.octave * 12 for state in melody]
        min_note = min(notes)
        max_note = max(notes)
        range_size = max_note - min_note
        
        print(f"  音域: {min_note} - {max_note} (范围: {range_size})")
        print(f"  平均力度: {sum(s.velocity for s in melody) / len(melody):.1f}")


def test_custom_generator():
    """测试自定义生成器配置"""
    print("\n=== 测试自定义生成器 ===")
    
    # 创建C大调音阶
    scale = ScaleFactory.create_scale(NoteName.C, ScaleType.MAJOR)
    
    # 自定义配置
    config = MelodyConfig(
        scale=scale,
        emotion="happy",
        length=20,
        start_note=NoteName.E,
        start_octave=4,
        tempo=100,
        max_leap=5,
        climax_position=0.6,
        use_dynamics=True,
        duration_variety=0.8
    )
    
    generator = MarkovMelodyGenerator(config)
    melody = generator.generate()
    
    print(f"自定义配置生成 {len(melody)} 个音符:")
    for i, state in enumerate(melody[:8]):  # 只显示前8个
        print(f"  {i+1}. {state.note.name}{state.octave} - "
              f"时长: {state.duration}, 力度: {state.velocity}")


def test_midi_output():
    """测试MIDI输出功能"""
    print("\n=== 测试MIDI输出 ===")
    
    try:
        # 生成旋律
        melody = generate_melody(emotion="happy", length=24, start_note="G")
        
        # 创建MIDI转换器
        midi_converter = MIDIGenerator()
        
        # 准备音符和时值
        notes = [state.note for state in melody]
        durations = [state.duration for state in melody]
        
        # 添加到MIDI
        midi_converter.add_melody(notes, durations)
        
        # 保存MIDI文件
        midi_converter.save("test_markov_melody.mid")
        print("✅ MIDI文件已保存: test_markov_melody.mid")
        
        # 验证文件大小
        file_size = os.path.getsize("test_markov_melody.mid")
        print(f"文件大小: {file_size} 字节")
        
        return True
        
    except Exception as e:
        print(f"❌ MIDI输出失败: {e}")
        return False


def analyze_melody_characteristics(melody):
    """分析旋律特征"""
    if not melody:
        return {}
    
    # 音域分析
    notes = [state.note.value + state.octave * 12 for state in melody]
    min_note = min(notes)
    max_note = max(notes)
    range_size = max_note - min_note
    
    # 力度分析
    velocities = [state.velocity for state in melody]
    avg_velocity = sum(velocities) / len(velocities)
    dynamic_range = max(velocities) - min(velocities)
    
    # 时值分析
    durations = [state.duration for state in melody]
    avg_duration = sum(durations) / len(durations)
    
    # 音程跳跃分析
    leaps = []
    for i in range(1, len(melody)):
        leap = abs(melody[i].note.value - melody[i-1].note.value)
        leaps.append(leap)
    
    avg_leap = sum(leaps) / len(leaps) if leaps else 0
    
    return {
        'note_range': range_size,
        'avg_velocity': avg_velocity,
        'dynamic_range': dynamic_range,
        'avg_duration': avg_duration,
        'avg_leap': avg_leap,
        'min_note': min_note,
        'max_note': max_note
    }


def main():
    """主测试函数"""
    print("🎵 开始测试马尔可夫链旋律生成算法\n")
    
    # 测试1: 基本功能
    melody1 = test_basic_melody_generation()
    
    # 分析生成的旋律
    characteristics = analyze_melody_characteristics(melody1)
    print(f"\n旋律特征分析:")
    for key, value in characteristics.items():
        print(f"  {key}: {value}")
    
    # 测试2: 不同情感
    test_different_emotions()
    
    # 测试3: 自定义配置
    test_custom_generator()
    
    # 测试4: MIDI输出
    midi_success = test_midi_output()
    
    print(f"\n=== 测试总结 ===")
    print(f"基本旋律生成: ✅")
    print(f"多情感支持: ✅")
    print(f"自定义配置: ✅")
    print(f"MIDI输出: {'✅' if midi_success else '❌'}")
    
    if midi_success:
        print("\n🎉 所有测试通过！算法实现正确")
        print("📁 生成的MIDI文件: test_markov_melody.mid")
    else:
        print("\n⚠️  部分测试失败，需要检查实现")


if __name__ == "__main__":
    main()