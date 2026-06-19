#!/usr/bin/env python3
"""
情感映射系统演示
展示调式/速度/音程范围 ↔ 情绪映射功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evo_music.emotion_mapping import EmotionMapper, EmotionType, get_emotion_mapper
from evo_music.emotion_mapping import create_emotion_aware_generator
from evo_music.midi_output import MIDIGenerator
import random


def demo_emotion_profiles():
    """演示情感特征配置"""
    print("🎭 情感特征配置演示")
    print("=" * 50)
    
    mapper = get_emotion_mapper()
    
    for emotion in EmotionType:
        profile = mapper.get_emotion_profile(emotion)
        
        print(f"\n🎵 {emotion.value} 情感:")
        print(f"   描述: {profile.description}")
        print(f"   速度范围: {profile.tempo_range} BPM")
        print(f"   音域范围: {profile.pitch_range} (MIDI)")
        print(f"   音符密度: {profile.note_density} 音符/小节")
        print(f"   力度范围: {profile.dynamic_range}")
        print(f"   跳跃频率: {profile.leap_frequency:.2f}")
        print(f"   高潮强度: {profile.climax_intensity:.2f}")
        print(f"   偏好调式: {profile.preferred_modes}")


def demo_emotion_mapping():
    """演示情感到参数的映射"""
    print("\n🔄 情感参数映射演示")
    print("=" * 50)
    
    mapper = get_emotion_mapper()
    
    # 测试不同情感的参数映射
    test_emotions = [EmotionType.HAPPY, EmotionType.SAD, EmotionType.EPIC, EmotionType.MYSTERIOUS]
    
    for emotion in test_emotions:
        print(f"\n--- {emotion.value} 情感参数 ---")
        params = mapper.map_emotion_to_params(emotion)
        
        print(f"  速度: {params['tempo']} BPM")
        print(f"  音域: {params['pitch_range']} (MIDI)")
        print(f"  密度: {params['note_density']:.1f} 音符/小节")
        print(f"  力度范围: {params['dynamic_range']}")
        print(f"  跳跃频率: {params['leap_frequency']:.2f}")
        print(f"  高潮强度: {params['climax_intensity']:.2f}")
        print(f"  音阶: {params['scale'].scale_type}")


def demo_custom_parameter_override():
    """演示自定义参数覆盖"""
    print("\n🎛️ 自定义参数覆盖演示")
    print("=" * 50)
    
    mapper = get_emotion_mapper()
    
    # 创建欢快情感，但使用自定义速度和音域
    custom_params = mapper.map_emotion_to_params(
        EmotionType.HAPPY,
        override_tempo=100,  # 比默认慢一些
        override_range=(55, 79)  # 比默认低一些的音域
    )
    
    print(f"🎵 自定义欢快情感:")
    print(f"   速度: {custom_params['tempo']} BPM (原始: 120-160)")
    print(f"   音域: {custom_params['pitch_range']} (原始: 60-84)")
    print(f"   其他参数保持默认")


def demo_melody_analysis():
    """演示旋律情感分析"""
    print("\n🎼 旋律情感分析演示")
    print("=" * 50)
    
    mapper = get_emotion_mapper()
    
    # 生成不同情感的旋律进行分析
    emotions_to_test = [EmotionType.HAPPY, EmotionType.SAD, EmotionType.MYSTERIOUS]
    
    for emotion in emotions_to_test:
        print(f"\n--- 分析 {emotion.value} 旋律 ---")
        
        # 生成旋律
        try:
            generator = create_emotion_aware_generator(emotion, length=16)
            melody = generator.generate()
            
            # 分析情感
            detected_emotion = mapper.analyze_emotion_from_melody(melody)
            
            print(f"  生成: {len(melody)} 个音符")
            print(f"  检测情感: {detected_emotion.value}")
            print(f"  匹配度: {'✅' if detected_emotion == emotion else '⚠️'}")
            
            # 保存MIDI文件
            midi_gen = MIDIGenerator()
            notes = [state.note for state in melody]
            durations = [state.duration for state in melody]
            midi_gen.add_melody(notes, durations)
            
            filename = f"demo_{emotion.value}_melody.mid"
            midi_gen.save(filename)
            print(f"  保存为: {filename}")
            
        except Exception as e:
            print(f"  ❌ 生成失败: {e}")


def demo_cross_emotion_comparison():
    """演示跨情感对比"""
    print("\n🔍 跨情感对比演示")
    print("=" * 50)
    
    mapper = get_emotion_mapper()
    
    # 对比不同情感的特征
    emotions = [EmotionType.HAPPY, EmotionType.SAD, EmotionType.EPIC]
    
    print(f"{'情感':<10} {'速度':<8} {'音域':<8} {'密度':<8} {'跳跃':<8}")
    print("-" * 50)
    
    for emotion in emotions:
        profile = mapper.get_emotion_profile(emotion)
        
        # 计算平均速度
        avg_tempo = sum(profile.tempo_range) / 2
        # 计算音域大小
        range_size = profile.pitch_range[1] - profile.pitch_range[0]
        # 格式化跳跃频率
        leap_freq = f"{profile.leap_frequency:.2f}"
        
        print(f"{emotion.value:<10} {avg_tempo:<8.0f} {range_size:<8} {profile.note_density:<8.1f} {leap_freq:<8}")


def demo_emotion_config_generation():
    """演示情感配置生成"""
    print("\n⚙️ 情感配置生成演示")
    print("=" * 50)
    
    mapper = get_emotion_mapper()
    
    # 为中国风情感生成完整配置
    chinese_config = mapper.generate_emotion_config(EmotionType.CHINESE)
    
    print(f"🎵 中国风情感配置:")
    print(f"   描述: {chinese_config['description']}")
    print(f"   速度: {chinese_config['tempo']} BPM")
    print(f"   音域: {chinese_config['pitch_range']}")
    print(f"   密度: {chinese_config['note_density']:.1f}")
    print(f"   力度范围: {chinese_config['dynamic_range']}")
    print(f"   生成参数:")
    for key, value in chinese_config['generation_params'].items():
        print(f"     {key}: {value}")


def main():
    """主演示函数"""
    print("🎭 情感映射系统 - 调式/速度/音程范围 ↔ 情绪映射")
    print("=" * 60)
    
    # 执行所有演示
    demo_emotion_profiles()
    demo_emotion_mapping()
    demo_custom_parameter_override()
    demo_melody_analysis()
    demo_cross_emotion_comparison()
    demo_emotion_config_generation()
    
    print(f"\n🎉 情感映射系统演示完成！")
    print("💡 生成的MIDI文件可以在音乐播放器中测试不同情感的差异")


if __name__ == "__main__":
    main()