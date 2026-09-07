"""
鼓点与节奏层 - 完整实现
生成匹配风格的鼓点pattern
支持多种音乐风格的鼓点生成
"""

import random
import sys
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# 导入现有模块
from evo_music.rhythm import TimeSignature, NoteDuration, NoteEvent, RhythmPattern, RhythmFactory
from dataclasses import dataclass, field
from typing import Optional

# 扩展NoteEvent类来支持鼓件类型
@dataclass
class DrumNoteEvent(NoteEvent):
    """鼓音符事件 - 扩展NoteEvent支持鼓件类型"""
    drum_type: Optional['DrumType'] = None  # 鼓件类型

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
class EmotionProfile:
    """情感配置"""
    energy: float = 0.5          # 能量水平 0-1
    valence: float = 0.5        # 情感极性 0-1 (负面-正面)
    intensity: float = 0.5      # 强度 0-1
    complexity: float = 0.5    # 复杂度 0-1

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
            if hasattr(event, 'drum_type') and event.drum_type:
                note = event.drum_type.get_midi_note()
                velocity = getattr(event, 'velocity', 80)
                midi_events.append((getattr(event, 'time', 0), 9, note, velocity))
        return midi_events
    
    def get_pattern_summary(self) -> Dict:
        """获取模式摘要"""
        return {
            "name": self.name,
            "style": self.style.value["name"],
            "tempo": self.tempo,
            "time_signature": self.time_signature.value,
            "events_count": len(self.events),
            "duration": sum(getattr(e, 'duration', 0) for e in self.events)
        }

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
            "soft_beat": self._create_soft_beat_pattern,
            "gentle_backbeat": self._create_gentle_backbeat_pattern,
            "quarter_notes": self._create_quarter_notes_pattern,
            "rock_eighth": self._create_rock_eighth_pattern,
            "jazz_triplet": self._create_jazz_triplet_pattern,
            "funk_sixteenth": self._create_funk_sixteenth_pattern,
            "disco_accent": self._create_disco_accent_pattern,
            "hiphop_triplet": self._create_hiphop_triplet_pattern,
            "jazz_swing": self._create_jazz_swing_pattern,
            "funk_offbeat": self._create_funk_offbeat_pattern,
        }
    
    def generate_drum_pattern(self, 
                            time_signature: TimeSignature = TimeSignature.FOUR_FOUR, 
                            style: StyleProfile = StyleProfile.POP,
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
        all_patterns = [kick_pattern, snare_pattern, hihat_pattern]
        for pattern in all_patterns:
            if isinstance(pattern, list):
                events.extend(pattern)
            else:
                events.extend(pattern.events if hasattr(pattern, 'events') else pattern)
        
        # 为每个事件添加鼓件类型
        events = self._assign_drum_types(events, style_config["name"])
        
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
    
    def generate_style_library(self) -> Dict[str, DrumPattern]:
        """生成风格库"""
        style_library = {}
        
        # 为每种风格生成示例鼓点
        for style in StyleProfile:
            # 使用中性情感配置
            emotion = EmotionProfile(energy=0.5, valence=0.5, intensity=0.5, complexity=0.5)
            
            pattern = self.generate_drum_pattern(
                time_signature=TimeSignature.FOUR_FOUR,
                style=style,
                emotion_profile=emotion,
                tempo=style.value["tempo_range"][0] + 10  # 取中速
            )
            
            style_library[style.value["name"]] = pattern
        
        return style_library
    
    # Pattern生成方法
    def _create_strong_beat_pattern(self) -> List[NoteEvent]:
        """强拍pattern"""
        events = [
            DrumNoteEvent(note_name=None, duration=0.0, velocity=95, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=0.5, velocity=70, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=70, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.5, velocity=70, drum_type=DrumType.HIHAT),
        ]
        return events
    
    def _create_backbeat_pattern(self) -> List[NoteEvent]:
        """反拍pattern"""
        events = [
            DrumNoteEvent(note_name=None, duration=1.0, velocity=85, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=3.0, velocity=85, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=0.0, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=0.5, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.5, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=2.0, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=2.5, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=3.0, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=3.5, velocity=65, drum_type=DrumType.HIHAT),
        ]
        return events
    
    def _create_steady_eighth_pattern(self) -> List[NoteEvent]:
        """稳定八分音符pattern"""
        events = []
        for i in range(8):
            events.append(DrumNoteEvent(note_name=None, duration=i * 0.25, velocity=60, drum_type=DrumType.HIHAT))
        return events
    
    def _create_rock_drive_pattern(self) -> List[NoteEvent]:
        """摇滚驱动pattern"""
        events = [
            DrumNoteEvent(note_name=None, duration=0.0, velocity=95, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=0.0, velocity=75, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=90, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=1.5, velocity=90, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=75, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=2.0, velocity=90, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=2.5, velocity=90, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=2.0, velocity=75, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=3.0, velocity=90, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=3.0, velocity=75, drum_type=DrumType.HIHAT),
        ]
        return events
    
    def _create_jazz_walk_pattern(self) -> List[NoteEvent]:
        """爵士walk pattern"""
        events = [
            DrumNoteEvent(note_name=None, duration=0.0, velocity=70, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=0.0, velocity=60, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=0.5, velocity=55, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=65, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=1.75, velocity=75, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=1.5, velocity=60, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=2.0, velocity=55, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=2.25, velocity=70, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=2.5, velocity=70, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=2.5, velocity=60, drum_type=DrumType.HIHAT),
        ]
        return events
    
    def _create_funk_syncopation_pattern(self) -> List[NoteEvent]:
        """放克切分pattern"""
        events = [
            DrumNoteEvent(note_name=None, duration=0.0, velocity=90, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=0.25, velocity=85, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=0.5, velocity=90, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=0.0, velocity=75, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=0.25, velocity=70, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=0.5, velocity=75, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=0.75, velocity=85, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=0.75, velocity=70, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=90, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=1.25, velocity=85, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=1.5, velocity=90, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=75, drum_type=DrumType.HIHAT),
        ]
        return events
    
    def _create_disco_four_on_floor_pattern(self) -> List[NoteEvent]:
        """迪斯科四拍pattern"""
        events = []
        for i in range(4):
            events.append(DrumNoteEvent(note_name=None, duration=i, velocity=85, drum_type=DrumType.KICK))
            events.append(DrumNoteEvent(note_name=None, duration=i, velocity=70, drum_type=DrumType.HIHAT))
            if i % 2 == 1:
                events.append(DrumNoteEvent(note_name=None, duration=i, velocity=80, drum_type=DrumType.SNARE))
        return events
    
    def _create_hiphop_syncopated_pattern(self) -> List[NoteEvent]:
        """嘻哈切分pattern"""
        events = [
            DrumNoteEvent(note_name=None, duration=0.0, velocity=90, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=0.75, velocity=85, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=0.5, velocity=80, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=1.5, velocity=80, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=0.0, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=0.33, velocity=60, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=0.67, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=60, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.33, velocity=65, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.67, velocity=60, drum_type=DrumType.HIHAT),
        ]
        return events
    
    def _create_soft_beat_pattern(self) -> List[NoteEvent]:
        """柔和拍子pattern"""
        events = [
            DrumNoteEvent(note_name=None, duration=0.0, velocity=70, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=2.0, velocity=70, drum_type=DrumType.KICK),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=60, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=3.0, velocity=60, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=0.0, velocity=50, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=1.0, velocity=50, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=2.0, velocity=50, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=3.0, velocity=50, drum_type=DrumType.HIHAT),
        ]
        return events
    
    def _create_gentle_backbeat_pattern(self) -> List[NoteEvent]:
        """柔和反拍pattern"""
        events = [
            DrumNoteEvent(note_name=None, duration=1.0, velocity=65, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=3.0, velocity=65, drum_type=DrumType.SNARE),
            DrumNoteEvent(note_name=None, duration=0.0, velocity=50, drum_type=DrumType.HIHAT),
            DrumNoteEvent(note_name=None, duration=2.0, velocity=50, drum_type=DrumType.HIHAT),
        ]
        return events
    
    def _create_quarter_notes_pattern(self) -> List[NoteEvent]:
        """四分音符pattern"""
        events = []
        for i in range(4):
            events.append(DrumNoteEvent(note_name=None, duration=i, velocity=55, drum_type=DrumType.HIHAT))
        return events
    
    def _create_rock_eighth_pattern(self) -> List[NoteEvent]:
        """摇滚八分音符pattern"""
        events = []
        for i in range(8):
            velocity = 80 if i % 2 == 0 else 60
            events.append(DrumNoteEvent(note_name=None, duration=i * 0.25, velocity=velocity, drum_type=DrumType.HIHAT))
        return events
    
    def _create_jazz_triplet_pattern(self) -> List[NoteEvent]:
        """爵士三连音pattern"""
        events = []
        for i in range(12):
            events.append(DrumNoteEvent(note_name=None, duration=i * 0.33, velocity=55, drum_type=DrumType.HIHAT))
        return events
    
    def _create_funk_sixteenth_pattern(self) -> List[NoteEvent]:
        """放克十六分音符pattern"""
        events = []
        for i in range(16):
            velocity = 75 if i % 4 == 0 else 65
            events.append(DrumNoteEvent(note_name=None, duration=i * 0.25, velocity=velocity, drum_type=DrumType.HIHAT))
        return events
    
    def _create_disco_accent_pattern(self) -> List[NoteEvent]:
        """迪斯科强调pattern"""
        events = []
        for i in range(4):
            events.append(NoteEvent(None, i, 75, drum_type=DrumType.KICK))
            if i == 2:
                events.append(NoteEvent(None, i, 85, drum_type=DrumType.SNARE))
            events.append(NoteEvent(None, i + 0.5, 65, drum_type=DrumType.HIHAT))
        return events
    
    def _create_hiphop_triplet_pattern(self) -> List[NoteEvent]:
        """嘻哈三连音pattern"""
        events = []
        for i in range(12):
            events.append(NoteEvent(None, i * 0.33, 60, drum_type=DrumType.HIHAT))
        return events
    
    def _create_jazz_swing_pattern(self) -> List[NoteEvent]:
        """爵士摇摆pattern"""
        events = []
        for i in range(8):
            if i % 2 == 0:
                events.append(NoteEvent(None, i * 0.5 + 0.1, 70, drum_type=DrumType.HIHAT))
            else:
                events.append(NoteEvent(None, i * 0.5 - 0.1, 60, drum_type=DrumType.HIHAT))
        return events
    
    def _create_funk_offbeat_pattern(self) -> List[NoteEvent]:
        """放克反拍pattern"""
        events = [
            NoteEvent(None, 0.5, 85, drum_type=DrumType.SNARE),
            NoteEvent(None, 1.5, 85, drum_type=DrumType.SNARE),
            NoteEvent(None, 2.5, 85, drum_type=DrumType.SNARE),
            NoteEvent(None, 3.5, 85, drum_type=DrumType.SNARE),
        ]
        return events
    
    # 辅助方法
    def _assign_drum_types(self, events: List[NoteEvent], style_name: str) -> List[NoteEvent]:
        """为事件分配鼓件类型"""
        # 这里简化处理，为不同风格分配不同的鼓件配置
        for event in events:
            if "kick" in event.note_name.lower() if event.note_name else "":
                event.drum_type = DrumType.KICK
            elif "snare" in event.note_name.lower() if event.note_name else "":
                event.drum_type = DrumType.SNARE
            elif "hihat" in event.note_name.lower() if event.note_name else "":
                event.drum_type = DrumType.HIHAT
            elif "crash" in event.note_name.lower() if event.note_name else "":
                event.drum_type = DrumType.CRASH
            else:
                # 默认分配
                if event.velocity > 80:
                    event.drum_type = DrumType.KICK
                elif event.velocity > 60:
                    event.drum_type = DrumType.SNARE
                else:
                    event.drum_type = DrumType.HIHAT
        return events
    
    def _add_accents(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """添加强调"""
        for event in events:
            if hasattr(event, 'velocity') and event.velocity:
                event.velocity = min(127, event.velocity + 10)
        return events
    
    def _add_variations(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """添加变化"""
        # 随机添加一些装饰音
        if random.random() < 0.3:
            events.append(NoteEvent(None, 0.0, 75, drum_type=DrumType.CRASH))
        if random.random() < 0.2:
            events.append(NoteEvent(None, 2.0, 70, drum_type=DrumType.RIDE))
        return events
    
    def _simplify_pattern(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """简化pattern"""
        # 只保留主要鼓件
        return [e for e in events if hasattr(e, 'drum_type') and e.drum_type in [DrumType.KICK, DrumType.SNARE, DrumType.HIHAT]]
    
    def _vary_velocity(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """变化velocity"""
        for event in events:
            if hasattr(event, 'velocity') and event.velocity and random.random() < 0.3:
                variation = random.uniform(0.8, 1.2)
                event.velocity = int(event.velocity * variation)
                event.velocity = max(20, min(127, event.velocity))
        return events
    
    def _vary_timing(self, events: List[NoteEvent]) -> List[NoteEvent]:
        """变化时间"""
        for event in events:
            if hasattr(event, 'time') and random.random() < 0.2:
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
            if hasattr(event, 'drum_type') and event.drum_type in instrument_map and random.random() < 0.3:
                event.drum_type = instrument_map[event.drum_type]
        return events
    
    def _adjust_for_emotion(self, events: List[NoteEvent], emotion: EmotionProfile) -> List[NoteEvent]:
        """根据情感调整鼓点"""
        # 高能量情感：增加velocity
        if emotion.energy > 0.7:
            for event in events:
                if hasattr(event, 'velocity') and event.velocity:
                    event.velocity = min(127, int(event.velocity * 1.2))
        
        # 低能量情感：减少velocity
        elif emotion.energy < 0.3:
            for event in events:
                if hasattr(event, 'velocity') and event.velocity:
                    event.velocity = max(40, int(event.velocity * 0.8))
        
        # 情感性情感：添加更多变化
        if emotion.valence < 0.3 and random.random() < 0.3:
            # 添加一些装饰音
            events.append(NoteEvent(None, 0.0, 60, drum_type=DrumType.CRASH))
        
        return events

# 全局实例
drum_generator = DrumLayerGenerator()

def test_drum_layer():
    """测试鼓点与节奏层"""
    print("=== 测试鼓点与节奏层完整实现 ===")
    
    # 测试生成风格库
    print("\n1. 生成风格库...")
    style_library = drum_generator.generate_style_library()
    
    for style_name, pattern in style_library.items():
        summary = pattern.get_pattern_summary()
        print(f"   ✅ {style_name}: {summary['events_count']}个事件, {summary['duration']:.1f}拍")
    
    # 测试情感调整
    print("\n2. 测试情感调整...")
    happy_emotion = EmotionProfile(energy=0.8, valence=0.9, intensity=0.7, complexity=0.5)
    sad_emotion = EmotionProfile(energy=0.2, valence=0.1, intensity=0.3, complexity=0.4)
    
    rock_pattern = drum_generator.generate_drum_pattern(
        time_signature=TimeSignature.FOUR_FOUR,
        style=StyleProfile.ROCK,
        emotion_profile=happy_emotion,
        tempo=120
    )
    
    print(f"   快乐摇滚模式: {rock_pattern.name}")
    print(f"   事件数量: {len(rock_pattern.events)}")
    
    # 测试变体生成
    print("\n3. 测试变体生成...")
    variations = drum_generator.create_style_variations(rock_pattern, 2)
    print(f"   生成了 {len(variations)} 个变体")
    
    # 测试MIDI输出
    print("\n4. 测试MIDI输出...")
    midi_events = rock_pattern.to_midi_events()
    print(f"   MIDI事件数量: {len(midi_events)}")
    
    print("\n✅ 所有测试通过！")
    return True

if __name__ == "__main__":
    test_drum_layer()