"""
鼓点与节奏层 - 生成匹配风格的鼓点pattern
支持多种音乐风格的鼓点生成
"""

import random
import sys
import os
sys.path.append(os.path.dirname(__file__))
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

from rhythm import TimeSignature, NoteDuration, NoteEvent, RhythmPattern, RhythmFactory
from emotion_mapping import EmotionProfile

# 简化导入，避免依赖问题
try:
    from music_theory import Note, Scale, Chord
except ImportError:
    # 创建简化的类以避免依赖问题
    @dataclass
    class Note:
        name: str
        octave: int = 4
    
    @dataclass
    class Scale:
        name: str
        notes: List[str]
    
    @dataclass 
    class Chord:
        name: str
        notes: List[str]

try:
    from emotion_mapping import EmotionProfile
except ImportError:
    # 创建简化的EmotionProfile
    @dataclass
    class EmotionProfile:
        energy: float = 0.5
        valence: float = 0.5
        arousal: float = 0.5
        intensity: float = 0.5


class DrumType(Enum):
    """鼓件类型"""
    KICK = "kick"          # 底鼓
    SNARE = "snare"        # 军鼓
    HIHAT = "hihat"        # 踩镲
    CRASH = "crash"        # 崩镲
    RIDE = "ride"          # 骑镲
    TOM1 = "tom1"          # 嗵嗵鼓1
    TOM2 = "tom2"          # 嗵嗵鼓2
    TOM3 = "tom3"          # 嗵嗵鼓3
    PERCUSSION = "percussion"  # 打击乐
    
    def get_midi_note(self) -> int:
        """获取MIDI音符编号"""
        notes = {
            DrumType.KICK: 36,
            DrumType.SNARE: 40,
            DrumType.HIHAT: 42,
            DrumType.CRASH: 49,
            DrumType.RIDE: 51,
            DrumType.TOM1: 45,
            DrumType.TOM2: 47,
            DrumType.TOM3: 50,
            DrumType.PERCUSSION: 39
        }
        return notes.get(self, 36)


class StyleProfile(Enum):
    """音乐风格配置"""
    POP = {
        "name": "流行",
        "tempo_range": (100, 140),
        "kick_pattern": "strong_beat",
        "snare_pattern": "backbeat",
        "hihat_pattern": "steady_eighth",
        "density": "medium"
    }
    
    ROCK = {
        "name": "摇滚",
        "tempo_range": (110, 160),
        "kick_pattern": "rock_drive",
        "snare_pattern": "strong_backbeat",
        "hihat_pattern": "rock_eighth",
        "density": "high"
    }
    
    JAZZ = {
        "name": "爵士",
        "tempo_range": (70, 200),
        "kick_pattern": "jazz_walk",
        "snare_pattern": "jazz_swing",
        "hihat_pattern": "jazz_triplet",
        "density": "medium"
    }
    
    FUNK = {
        "name": "放克",
        "tempo_range": (90, 130),
        "kick_pattern": "funk_syncopation",
        "snare_pattern": "funk_offbeat",
        "hihat_pattern": "funk_sixteenth",
        "density": "high"
    }
    
    BALLAD = {
        "name": "抒情",
        "tempo_range": (60, 100),
        "kick_pattern": "soft_beat",
        "snare_pattern": "gentle_backbeat",
        "hihat_pattern": "quarter_notes",
        "density": "low"
    }
    
    DISCO = {
        "name": "迪斯科",
        "tempo_range": (110, 130),
        "kick_pattern": "disco_four_on_floor",
        "snare_pattern": "disco_accent",
        "hihat_pattern": "disco_eighth",
        "density": "medium"
    }
    
    HIPHOP = {
        "name": "嘻哈",
        "tempo_range": (80, 120),
        "kick_pattern": "hiphop_syncopated",
        "snare_pattern": "hiphop_backbeat",
        "hihat_pattern": "hiphop_triplet",
        "density": "medium"
    }


@dataclass
class DrumPattern:
    """鼓点模式"""
    name: str
    time_signature: TimeSignature
    style: StyleProfile
    tempo: int
    events: List[NoteEvent]
    description: str = ""
    emotion_profile: Optional[EmotionProfile] = None
    
    def to_midi_events(self) -> List[Tuple[int, int, int, int]]:
        """转换为MIDI事件列表 (时间, 通道, 音符, 速度)"""
        midi_events = []
        for event in self.events:
            if event.drum_type:
                note = event.drum_type.get_midi_note()
                velocity = event.velocity or 80
                midi_events.append((event.time, 9, note, velocity))
        return midi_events


class DrumLayerGenerator:
    """鼓点与节奏层生成器"""
    
    def __init__(self):
        self.pattern_templates = {
            "strong_beat": self._create_strong_beat_pattern,
            "backbeat": self._create_backbeat_pattern,
            "steady_eighth": self._create_steady_eighth_pattern,
            "rock_drive": self._create_rock_drive_pattern,
            "jazz_walk": self._create_jazz_walk_pattern,
            "funk_syncopation": self._create_funk_syncopation_pattern,
            "disco_four_on_floor": self._create_disco_four_on_floor_pattern,
            "hiphop_syncopated": self._create_hiphop_syncopated_pattern,
        }
    
    def generate_drum_pattern(self, 
                            time_signature: TimeSignature, 
                            style: StyleProfile,
                            emotion_profile: Optional[EmotionProfile] = None,
                            tempo: int = 120) -> DrumPattern:
        """生成鼓点模式"""
        
        # 根据风格设置默认tempo范围
        style_config = style.value
        if tempo < style_config["tempo_range"][0]:
            tempo = style_config["tempo_range"][0]
        elif tempo > style_config["tempo_range"][1]:
            tempo = style_config["tempo_range"][1]
        
        # 生成基础鼓点pattern
        events = []
        
        # 根据风格生成不同pattern
        kick_pattern = self.pattern_templates[style_config["kick_pattern"]]()
        snare_pattern = self.pattern_templates[style_config["snare_pattern"]]()
        hihat_pattern = self.pattern_templates[style_config["hihat_pattern"]]()
        
        # 根据密度调整复杂度
        density = style_config["density"]
        if density == "high":
            # 高密度：添加更多装饰音
            kick_pattern = self._add_accents(kick_pattern)
            snare_pattern = self._add_accents(snare_pattern)
            hihat_pattern = self._add_variations(hihat_pattern)
        elif density == "low":
            # 低密度：简化pattern
            kick_pattern = self._simplify_pattern(kick_pattern)
            snare_pattern = self._simplify_pattern(snare_pattern)
            hihat_pattern = self._simplify_pattern(hihat_pattern)
        
        # 合并所有鼓件
        for pattern in [kick_pattern, snare_pattern, hihat_pattern]:
            events.extend(pattern)
        
        # 根据情感调整velocity
        if emotion_profile:
            events = self._adjust_for_emotion(events, emotion_profile)
        
        # 创建DrumPattern对象
        pattern_name = f"{style.value['name']} 鼓点模式"
        description = f"{style.value['name']}风格的鼓点节奏，tempo={tempo}BPM"
        
        return DrumPattern(
            name=pattern_name,
            time_signature=time_signature,
            style=style,
            tempo=tempo,
            events=events,
            description=description,
            emotion_profile=emotion_profile
        )
    
    def create_style_variations(self, 
                               base_pattern: DrumPattern, 
                               variation_count: int = 3) -> List[DrumPattern]:
        """创建风格变体"""
        variations = []
        
        for i in range(variation_count):
            # 复制基础pattern
            variation_events = base_pattern.events.copy()
            
            # 随机变化
            if i % 3 == 0:
                # 变化velocity
                variation_events = self._vary_velocity(variation_events)
            elif i % 3 == 1:
                # 变化节奏
                variation_events = self._vary_timing(variation_events)
            else:
                # 变化鼓件配置
                variation_events = self._vary_instruments(variation_events)
            
            variation_name = f"{base_pattern.name} 变体{i+1}"
            variations.append(DrumPattern(
                name=variation_name,
                time_signature=base_pattern.time_signature,
                style=base_pattern.style,
                tempo=base_pattern.tempo,
                events=variation_events,
                description=f"{base_pattern.description} - 变体{i+1}"
            ))
        
        return variations
    
    # Pattern生成方法
    def _create_strong_beat_pattern(self) -> List[NoteEvent]:
        """强拍pattern"""
        events = [
            NoteEvent(DrumType.KICK, 0.0, 95),
            NoteEvent(DrumType.HIHAT, 0.0, 70),
            NoteEvent(DrumType.HIHAT, 0.5, 70),
            NoteEvent(DrumType.HIHAT, 1.0, 70),
            NoteEvent(DrumType.HIHAT, 1.5, 70),
        ]
        return events
    
    def _create_backbeat_pattern(self) -> List[NoteEvent]:
        """反拍pattern"""
        events = [
            NoteEvent(DrumType.SNARE, 1.0, 85),
            NoteEvent(DrumType.SNARE, 3.0, 85),
            NoteEvent(DrumType.HIHAT, 0.0, 65),
            NoteEvent(DrumType.HIHAT, 0.5, 65),
            NoteEvent(DrumType.HIHAT, 1.0, 65),
            NoteEvent(DrumType.HIHAT, 1.5, 65),
            NoteEvent(DrumType.HIHAT, 2.0, 65),
            NoteEvent(DrumType.HIHAT, 2.5, 65),
            NoteEvent(DrumType.HIHAT, 3.0, 65),
            NoteEvent(DrumType.HIHAT, 3.5, 65),
        ]
        return events
    
    def _create_steady_eighth_pattern(self) -> List[NoteEvent]:
        """稳定八分音符pattern"""
        events = []
        for i in range(8):
            events.append(NoteEvent(DrumType.HIHAT, i * 0.25, 60))
        return events
    
    def _create_rock_drive_pattern(self) -> List[NoteEvent]:
        """摇滚驱动pattern"""
        events = [
            NoteEvent(DrumType.KICK, 0.0, 95),
            NoteEvent(DrumType.HIHAT, 0.0, 75),
            NoteEvent(DrumType.SNARE, 1.0, 90),
            NoteEvent(DrumType.KICK, 1.5, 90),
            NoteEvent(DrumType.HIHAT, 1.0, 75),
            NoteEvent(DrumType.SNARE, 2.0, 90),
            NoteEvent(DrumType.KICK, 2.5, 90),
            NoteEvent(DrumType.HIHAT, 2.0, 75),
            NoteEvent(DrumType.SNARE, 3.0, 90),
            NoteEvent(DrumType.HIHAT, 3.0, 75),
        ]
        return events
    
    def _create_jazz_walk_pattern(self) -> List[NoteEvent]:
        """爵士walk pattern"""
        events = [
            NoteEvent(DrumType.KICK, 0.0, 70),
            NoteEvent(DrumType.HIHAT, 0.0, 60),
            NoteEvent(DrumType.HIHAT, 0.5, 55),
            NoteEvent(DrumType.SNARE, 1.0, 65),
            NoteEvent(DrumType.KICK, 1.75, 75),
            NoteEvent(DrumType.HIHAT, 1.5, 60),
            NoteEvent(DrumType.HIHAT, 2.0, 55),
            NoteEvent(DrumType.SNARE, 2.25, 70),
            NoteEvent(DrumType.KICK, 2.5, 70),
            NoteEvent(DrumType.HIHAT, 2.5, 60),
        ]
        return events
    
    def _create_funk_syncopation_pattern(self) -> List[NoteEvent]:
        """放克切分pattern"""
        events = [
            NoteEvent(DrumType.KICK, 0.0, 90),
            NoteEvent(DrumType.KICK, 0.25, 85),
            NoteEvent(DrumType.KICK, 0.5, 90),
            NoteEvent(DrumType.HIHAT, 0.0, 75),
            NoteEvent(DrumType.HIHAT, 0.25, 70),
            NoteEvent(DrumType.HIHAT, 0.5, 75),
            NoteEvent(DrumType.SNARE, 0.75, 85),
            NoteEvent(DrumType.HIHAT, 0.75, 70),
            NoteEvent(DrumType.KICK, 1.0, 90),
            NoteEvent(DrumType.KICK, 1.25, 85),
            NoteEvent(DrumType.KICK, 1.5, 90),
            NoteEvent(DrumType.HIHAT, 1.0, 75),
        ]
        return events
    
    def _create_disco_four_on_floor_pattern(self) -> List[NoteEvent]:
        """迪斯科四拍pattern"""
        events = []
        for i in range(4):
            events.append(NoteEvent(DrumType.KICK, i, 85))
            events.append(NoteEvent(DrumType.HIHAT, i, 70))
            if i % 2 == 1:
                events.append(NoteEvent(DrumType.SNARE, i, 80))
        return events
    
    def _create_hiphop_syncopated_pattern(self) -> List[NoteEvent]:
        """嘻哈切分pattern"""
        events = [
            NoteEvent(DrumType.KICK, 0.0, 90),
            NoteEvent(DrumType.KICK, 0.75, 85),
            NoteEvent(DrumType.SNARE, 0.5, 80),
            NoteEvent(DrumType.SNARE, 1.5, 80),
            NoteEvent(DrumType.HIHAT, 0.0, 65),
            NoteEvent(DrumType.HIHAT, 0.33, 60),
            NoteEvent(DrumType.HIHAT, 0.67, 65),
            NoteEvent(DrumType.HIHAT, 1.0, 60),
            NoteEvent(DrumType.HIHAT, 1.33, 65),
            NoteEvent(DrumType.HIHAT, 1.67, 60),
        ]
        return events
    
    # 辅助方法
    def _add_accents(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """添加强调"""
        for event in events:
            if event.velocity:
                event.velocity = min(127, event.velocity + 10)
        return events
    
    def _add_variations(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """添加变化"""
        # 随机添加一些装饰音
        if random.random() < 0.3:
            events.append(NoteEvent(DrumType.CRASH, 0.0, 75))
        if random.random() < 0.2:
            events.append(NoteEvent(DrumType.RIDE, 2.0, 70))
        return events
    
    def _simplify_pattern(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """简化pattern"""
        # 只保留主要鼓件
        return [e for e in events if e.drum_type in [DrumType.KICK, DrumType.SNARE, DrumType.HIHAT]]
    
    def _vary_velocity(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """变化velocity"""
        for event in events:
            if event.velocity and random.random() < 0.3:
                variation = random.uniform(0.8, 1.2)
                event.velocity = int(event.velocity * variation)
                event.velocity = max(20, min(127, event.velocity))
        return events
    
    def _vary_timing(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """变化时间"""
        for event in events:
            if random.random() < 0.2:
                variation = random.uniform(-0.1, 0.1)
                event.time = max(0, min(4.0, event.time + variation))
        return events
    
    def _vary_instruments(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """变化乐器"""
        instrument_map = {
            DrumType.HIHAT: DrumType.RIDE,
            DrumType.SNARE: DrumType.TOM1,
            DrumType.KICK: DrumType.TOM2,
        }
        
        for event in events:
            if event.drum_type in instrument_map and random.random() < 0.3:
                event.drum_type = instrument_map[event.drum_type]
        return events
    
    def _adjust_for_emotion(self, events: List[NoteEvent], emotion: EmotionProfile) -> List[NoteEvent]:
        """根据情感调整鼓点"""
        # 高能量情感：增加velocity
        if emotion.energy > 0.7:
            for event in events:
                if event.velocity:
                    event.velocity = min(127, int(event.velocity * 1.2))
        
        # 低能量情感：减少velocity
        elif emotion.energy < 0.3:
            for event in events:
                if event.velocity:
                    event.velocity = max(40, int(event.velocity * 0.8))
        
        # 情感性情感：添加更多变化
        if emotion.valence < 0.3 and random.random() < 0.3:
            # 添加一些装饰音
            events.append(NoteEvent(DrumType.CRASH, 0.0, 60))
        
        return events


# 测试函数
def test_drum_layer():
    """测试鼓点与节奏层"""
    print("=== 测试鼓点与节奏层 ===")
    
    generator = DrumLayerGenerator()
    
    # 测试不同风格的鼓点生成
    styles = [StyleProfile.POP, StyleProfile.ROCK, StyleProfile.JAZZ, StyleProfile.FUNK]
    
    for style in styles:
        print(f"\n--- {style.value['name']}风格鼓点 ---")
        
        # 生成基础鼓点
        drum_pattern = generator.generate_drum_pattern(
            TimeSignature.FOUR_FOUR,
            style,
            tempo=120
        )
        
        print(f"Pattern名称: {drum_pattern.name}")
        print(f"Tempo: {drum_pattern.tempo} BPM")
        print(f"事件数量: {len(drum_pattern.events)}")
        
        # 显示事件
        for event in drum_pattern.events[:5]:  # 只显示前5个
            print(f"  {event.time:.2f}s: {event.drum_type.value} - velocity {event.velocity}")
        
        # 创建变体
        variations = generator.create_style_variations(drum_pattern, 2)
        print(f"生成了 {len(variations)} 个变体")


if __name__ == "__main__":
    test_drum_layer()