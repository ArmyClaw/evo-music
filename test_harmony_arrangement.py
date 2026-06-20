#!/usr/bin/env python3
"""
测试和声编排功能 - 演示如何根据旋律自动生成和声
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from evo_music.harmony_arranger import HarmonyArranger, HarmonyConfig, HarmonyStyle
from evo_music.scales import ScaleFactory, ScaleType
from evo_music.melody import EmotionType
from evo_music.notes import NoteName


def test_harmony_arrangement():
    """测试和声编排功能"""
    print("🎵 开始测试和声编排功能...")
    
    # 创建和声编排器配置
    config = HarmonyConfig(
        style=HarmonyStyle.POP,
        chord_density=0.3,
        voice_leading=True,
        use_inversions=True,
        extensions_level=1,
        bass_walk=False,
        pad_voices=2
    )
    
    # 创建和声编排器
    arranger = HarmonyArranger(config)
    
    # 创建调式（C大调）
    scale_factory = ScaleFactory()
    c_major = scale_factory.create_scale(NoteName.C, ScaleType.MAJOR)  # C大调
    
    # 示例旋律：简单的主旋律
    melody_notes = [
        (60, 2),  # C4, 2拍
        (64, 1),  # E4, 1拍
        (67, 1),  # G4, 1拍
        (60, 2),  # C4, 2拍
        (62, 1),  # D4, 1拍
        (64, 1),  # E4, 1拍
        (60, 2),  # C4, 2拍
        (65, 1),  # F4, 1拍
        (67, 1),  # G4, 1拍
        (60, 2),  # C4, 2拍
    ]
    
    print(f"🎼 输入旋律：{len(melody_notes)} 个音符")
    for i, (note, duration) in enumerate(melody_notes):
        note_name = get_note_name(note)
        print(f"  音符 {i+1}: {note_name} ({duration} 拍)")
    
    print("\n🔧 开始生成和声...")
    
    # 生成和声编排
    result = arranger.arrange_harmony_for_melody(melody_notes, c_major)
    
    # 显示结果
    print("\n🎹 生成的和声编排结果：")
    print(f"  和弦风格: {config.style.value}")
    print(f"  和弦密度: {config.chord_density}")
    print(f"  扩展音级别: {config.extensions_level}")
    
    print("\n🎵 和弦进行：")
    for i, chord_info in enumerate(result["chord_progression"]):
        chord = chord_info["chord"]
        measure = chord_info["measure"]
        print(f"  小节 {measure+1}: {chord.name}")
    
    print("\n🎼 各声部音符：")
    
    # 和声声部
    if "harmony" in result["harmony_voices"]:
        print("  和声声部:")
        for i, (note, duration) in enumerate(result["harmony_voices"]["harmony"]):
            note_name = get_note_name(note)
            print(f"    {note_name} ({duration} 拍)")
    
    # 低音声部
    if "bass" in result["harmony_voices"]:
        print("  低音声部:")
        for i, (note, duration) in enumerate(result["harmony_voices"]["bass"]):
            note_name = get_note_name(note)
            print(f"    {note_name} ({duration} 拍)")
    
    # 垫底声部
    for i in range(config.pad_voices):
        if f"pad_{i}" in result["harmony_voices"]:
            print(f"  垫底声部 {i+1}:")
            for j, (note, duration) in enumerate(result["harmony_voices"][f"pad_{i}"]):
                note_name = get_note_name(note)
                print(f"    {note_name} ({duration} 拍)")
    
    print("\n🎯 旋律分析：")
    analysis = result["melody_analysis"]
    print(f"  音域范围: {analysis['pitch_range']} 半音")
    print(f"  关键音符数: {len(analysis['climax_notes'])}")
    print(f"  平均时值: {analysis['average_duration']:.1f} 拍")
    
    return result


def test_different_emotions():
    """测试不同情感的和声编排"""
    print("\n🎭 测试不同情感的和声编排...")
    
    # 测试不同情感
    emotions = [EmotionType.HAPPY, EmotionType.SAD, EmotionType.EPIC, EmotionType.PEACEFUL]
    
    for emotion in emotions:
        print(f"\n🎼 {emotion.value} 情感测试:")
        
        # 根据情感创建配置
        config = HarmonyConfig.get_default_for_emotion(emotion)
        arranger = HarmonyArranger(config)
        
        # 简单旋律
        melody_notes = [
            (60, 2),  # C4
            (64, 2),  # E4
            (67, 2),  # G4
            (60, 2),  # C4
        ]
        
        # 创建调式
        scale_factory = ScaleFactory()
        c_major = scale_factory.create_scale(NoteName.C, ScaleType.MAJOR)
        
        # 生成和声
        result = arranger.arrange_harmony_for_melody(melody_notes, c_major)
        
        # 显示主要和弦
        chord_names = [chord_info["chord"].name for chord_info in result["chord_progression"]]
        print(f"  生成和弦: {' → '.join(chord_names)}")


def get_note_name(note_value: int) -> str:
    """将音符数值转换为音符名称"""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = note_value // 12 - 1
    note_name = note_names[note_value % 12]
    return f"{note_name}{octave}"


def create_demo_midi():
    """创建演示MIDI文件"""
    print("\n🎹 创建演示MIDI文件...")
    
    try:
        from evo_music.midi_output import MIDIWriter
        
        # 创建配置
        config = HarmonyConfig(style=HarmonyStyle.POP)
        arranger = HarmonyArranger(config)
        
        # 创建旋律
        melody_notes = [
            (60, 2), (64, 1), (67, 1), (60, 2),  # 小节1
            (62, 1), (64, 1), (60, 2), (65, 1), (67, 1), (60, 2),  # 小节2
        ]
        
        # 生成和声
        scale_factory = ScaleFactory()
        c_major = scale_factory.create_scale(NoteName.C, ScaleType.MAJOR)
        result = arranger.arrange_harmony_for_melody(melody_notes, c_major)
        
        # 创建MIDI文件
        midi_writer = MIDIWriter()
        
        # 添加旋律声部
        midi_writer.add_track("Melody", melody_notes, channel=0, instrument=1)
        
        # 添加和声声部
        if "harmony" in result["harmony_voices"]:
            midi_writer.add_track("Harmony", result["harmony_voices"]["harmony"], channel=1, instrument=2)
        
        # 添加低音声部
        if "bass" in result["harmony_voices"]:
            midi_writer.add_track("Bass", result["harmony_voices"]["bass"], channel=2, instrument=3)
        
        # 保存文件
        midi_writer.save("demo_harmony_arrangement.mid")
        print("  ✅ 演示MIDI文件已保存: demo_harmony_arrangement.mid")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 创建MIDI文件失败: {e}")
        return False


def main():
    """主函数"""
    print("🎵 和声自动编排系统测试")
    print("=" * 50)
    
    # 基本测试
    try:
        result = test_harmony_arrangement()
        print("\n✅ 基本测试通过")
    except Exception as e:
        print(f"\n❌ 基本测试失败: {e}")
        return
    
    # 情感测试
    try:
        test_different_emotions()
        print("\n✅ 情感测试通过")
    except Exception as e:
        print(f"\n❌ 情感测试失败: {e}")
    
    # MIDI演示
    try:
        create_demo_midi()
        print("\n✅ 演示创建完成")
    except Exception as e:
        print(f"\n❌ 演示创建失败: {e}")
    
    print("\n🎉 所有测试完成！")


if __name__ == "__main__":
    main()