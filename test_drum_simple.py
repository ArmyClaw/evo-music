#!/usr/bin/env python3
"""
简单测试鼓点与节奏层功能
"""

import sys
import os
import os.path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 简化测试 - 直接使用rhythm模块中的类
from evo_music.rhythm import TimeSignature, NoteEvent, RhythmPattern, RhythmFactory
from evo_music.drum_layer import DrumType

def test_basic_rhythm():
    """测试基础节奏功能"""
    print("=== 测试基础节奏功能 ===")
    
    # 创建基础节奏模式
    rock_beat = RhythmFactory.create_rock_beat()
    print(f"摇滚节奏: {rock_beat.name}")
    print(f"BPM: {rock_beat.bpm}")
    print(f"拍号: {rock_beat.time_signature.value}")
    print(f"拍数: {rock_beat.get_total_beats()}")
    print(f"小节数: {rock_beat.get_duration()}")
    
    # 分析节奏模式
    from evo_music.rhythm import RhythmAnalyzer
    analysis = RhythmAnalyzer.analyze_pattern(rock_beat)
    print(f"分析结果: {analysis}")
    
    return True

def test_drum_instruments():
    """测试鼓件"""
    print("\n=== 测试鼓件 ===")
    
    # 测试各种鼓件的MIDI音符
    for drum_type in DrumType:
        midi_note = drum_type.get_midi_note()
        print(f"{drum_type.value}: MIDI {midi_note}")
    
    return True

def create_drum_pattern_manually():
    """手动创建一个鼓点模式"""
    print("\n=== 手动创建鼓点模式 ===")
    
    # 创建一个简单的鼓点模式
    events = [
        NoteEvent(DrumType.KICK, 0.0, 95),
        NoteEvent(DrumType.HIHAT, 0.0, 70),
        NoteEvent(DrumType.HIHAT, 0.5, 70),
        NoteEvent(DrumType.KICK, 1.0, 85),
        NoteEvent(DrumType.SNARE, 1.0, 90),
        NoteEvent(DrumType.HIHAT, 1.0, 70),
        NoteEvent(DrumType.HIHAT, 1.5, 70),
        NoteEvent(DrumType.KICK, 2.0, 90),
        NoteEvent(DrumType.SNARE, 2.0, 85),
        NoteEvent(DrumType.HIHAT, 2.0, 70),
        NoteEvent(DrumType.HIHAT, 2.5, 70),
        NoteEvent(DrumType.KICK, 3.0, 85),
        NoteEvent(DrumType.SNARE, 3.0, 90),
        NoteEvent(DrumType.HIHAT, 3.0, 70),
        NoteEvent(DrumType.HIHAT, 3.5, 70),
    ]
    
    pattern = RhythmPattern(
        name="手动鼓点",
        time_signature=TimeSignature.FOUR_FOUR,
        note_events=events,
        bpm=120,
        description="手动创建的鼓点模式"
    )
    
    print(f"创建的鼓点模式: {pattern.name}")
    print(f"事件数量: {len(pattern.note_events)}")
    print(f"总拍数: {pattern.get_total_beats()}")
    
    return pattern

def main():
    """主测试函数"""
    print("开始测试鼓点与节奏层功能...")
    
    try:
        # 测试基础节奏
        test_basic_rhythm()
        
        # 测试鼓件
        test_drum_instruments()
        
        # 创建鼓点模式
        pattern = create_drum_pattern_manually()
        
        print("\n✅ 所有测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)