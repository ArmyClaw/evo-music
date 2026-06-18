"""
节奏系统 - 节奏模式和节拍器
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import time


class TimeSignature(Enum):
    """拍号"""
    FOUR_FOUR = "4/4"          # 4/4拍
    THREE_FOUR = "3/4"         # 3/4拍
    TWO_FOUR = "2/4"          # 2/4拍
    SIX_EIGHT = "6/8"         # 6/8拍
    TWELVE_EIGHT = "12/8"     # 12/8拍

    @property
    def beats_per_measure(self) -> int:
        """每小节拍数"""
        return int(self.value.split('/')[0])
    
    @property
    def beat_value(self) -> int:
        """拍子的时值（以四分音符为单位）"""
        return 4 // int(self.value.split('/')[1])
    
    @property
    def measure_duration(self) -> float:
        """每小节时长（四分音符）"""
        return self.beats_per_measure


class NoteDuration(Enum):
    """音符时值（以四分音符为单位）"""
    WHOLE = 4.0                # 全音符
    HALF = 2.0                 # 二分音符
    QUARTER = 1.0             # 四分音符
    EIGHTH = 0.5               # 八分音符
    SIXTEENTH = 0.25          # 十六分音符
    THIRTY_SECOND = 0.125     # 三十二分音符
    SIXTY_FOURTH = 0.0625      # 六十四分音符


class NoteValue:
    """音符符号"""
    SYMBOLS = {
        NoteDuration.WHOLE: "𝅝",
        NoteDuration.HALF: "𝅗𝅥",
        NoteDuration.QUARTER: "♩",
        NoteDuration.EIGHTH: "♪",
        NoteDuration.SIXTEENTH: "♬",
        NoteDuration.THIRTY_SECOND: "♩𝄽",
        NoteDuration.SIXTY_FOURTH: "♪𝄽",
    }
    
    RESTS = {
        NoteDuration.WHOLE: "𝄻",
        NoteDuration.HALF: "𝄼",
        NoteDuration.QUARTER: "𝄽",
        NoteDuration.EIGHTH: "𝄾",
        NoteDuration.SIXTEENTH: "𝄿",
        NoteDuration.THIRTY_SECOND: "𝅀",
        NoteDuration.SIXTY_FOURTH: "𝅁",
    }


@dataclass
class NoteEvent:
    """音符事件"""
    note_name: Optional[str]    # 音名（None为休止符）
    duration: float             # 时值（以四分音符为单位）
    velocity: int = 80         # 力度（0-127）
    tie: bool = False           # 是否延音
    dotted: bool = False       # 是否附点
    triplet: bool = False      # 是否为三连音
    
    def get_total_duration(self) -> float:
        """获取总时长（考虑附点和三连音）"""
        duration = self.duration
        if self.dotted:
            duration *= 1.5
        if self.triplet:
            duration *= 2/3
        return duration
    
    def get_symbol(self) -> str:
        """获取音符符号"""
        if self.note_name is None:
            # 休止符
            for dur, symbol in NoteValue.RESTS.items():
                if abs(self.duration - dur.value) < 0.01:
                    return symbol
            return "𝄽"  # 默认四分休止符
        else:
            # 音符
            for dur, symbol in NoteValue.SYMBOLS.items():
                if abs(self.duration - dur.value) < 0.01:
                    return symbol
            return "♩"  # 默认四分音符
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "note": self.note_name,
            "duration": self.duration,
            "velocity": self.velocity,
            "tie": self.tie,
            "dotted": self.dotted,
            "triplet": self.triplet,
            "total_duration": self.get_total_duration(),
            "symbol": self.get_symbol()
        }


@dataclass
class RhythmPattern:
    """节奏模式"""
    name: str                        # 模式名称（如："Rock Beat"）
    time_signature: TimeSignature    # 拍号
    note_events: List[NoteEvent]     # 音符事件列表
    bpm: int = 120                   # 速度
    description: str = ""            # 描述
    
    def get_duration(self) -> float:
        """获取模式总时长（小节数）"""
        total_duration = sum(event.get_total_duration() for event in self.note_events)
        return total_duration / self.time_signature.beats_per_measure
    
    def get_total_beats(self) -> float:
        """获取总拍数"""
        return sum(event.get_total_duration() for event in self.note_events)
    
    def repeat(self, times: int) -> 'RhythmPattern':
        """重复节奏模式"""
        repeated_events = []
        for _ in range(times):
            repeated_events.extend(self.note_events)
        
        return RhythmPattern(
            name=f"{self.name} (x{times})",
            time_signature=self.time_signature,
            note_events=repeated_events,
            bpm=self.bpm,
            description=f"{self.description} (重复{times}次)"
        )
    
    def add_accent(self, beat_positions: List[int]) -> 'RhythmPattern':
        """在指定拍子上添加重音"""
        accented_events = []
        
        current_beat = 0
        for event in self.note_events:
            # 检查是否在指定的重音拍子上
            if current_beat in beat_positions:
                accented_events.append(NoteEvent(
                    note_name=event.note_name,
                    duration=event.duration,
                    velocity=min(127, event.velocity + 20),  # 增加力度
                    tie=event.tie,
                    dotted=event.dotted,
                    triplet=event.triplet
                ))
            else:
                accented_events.append(event)
            
            current_beat += event.get_total_duration()
        
        return RhythmPattern(
            name=f"{self.name} (accented)",
            time_signature=self.time_signature,
            note_events=accented_events,
            bpm=self.bpm,
            description=f"{self.description} (重音拍子: {beat_positions})"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "time_signature": self.time_signature.value,
            "note_events": [event.to_dict() for event in self.note_events],
            "bpm": self.bpm,
            "description": self.description,
            "duration_beats": self.get_total_beats(),
            "duration_measures": self.get_duration()
        }


class Metronome:
    """节拍器类"""
    
    def __init__(self, bpm: int = 120, time_signature: TimeSignature = TimeSignature.FOUR_FOUR):
        self.bpm = bpm
        self.time_signature = time_signature
        self.current_beat = 0
        self.is_running = False
        self.start_time = 0
        
    def get_beat_interval(self) -> float:
        """获取节拍间隔（秒）"""
        return 60.0 / self.bpm
    
    def next_beat(self) -> int:
        """下一拍，返回当前拍号（1-based）"""
        beats_per_measure = self.time_signature.beats_per_measure
        beat_number = (self.current_beat % beats_per_measure) + 1
        
        # 更新时间戳
        if self.is_running:
            elapsed = time.time() - self.start_time
            expected_beats = elapsed / self.get_beat_interval()
            self.current_beat = int(expected_beats)
        
        return beat_number
    
    def start(self):
        """开始节拍"""
        self.is_running = True
        self.start_time = time.time()
        self.current_beat = 0
    
    def stop(self):
        """停止节拍"""
        self.is_running = False
    
    def reset(self):
        """重置节拍器"""
        self.current_beat = 0
        self.is_running = False


class RhythmFactory:
    """节奏工厂类"""
    
    @staticmethod
    def create_rock_beat(time_signature: TimeSignature = TimeSignature.FOUR_FOUR, bpm: int = 120) -> RhythmPattern:
        """创建摇滚节奏"""
        events = [
            NoteEvent(None, 1.0, 80),    # 底鼓（四分音符）
            NoteEvent(None, 0.5, 60),     # 军鼓（八分音符）
            NoteEvent(None, 0.5, 100),    # 踩镲（八分音符）
        ]
        
        # 重复这个模式4次
        pattern = RhythmPattern(
            name="Rock Beat",
            time_signature=time_signature,
            note_events=events,
            bpm=bpm,
            description="经典摇滚节奏：底鼓-军鼓-踩镲"
        )
        
        return pattern.repeat(4)
    
    @staticmethod
    def create_waltz(time_signature: TimeSignature = TimeSignature.THREE_FOUR, bpm: int = 100) -> RhythmPattern:
        """创建华尔兹节奏"""
        events = [
            NoteEvent(None, 1.0, 80),    # 第一拍强音
            NoteEvent(None, 0.5, 60),    # 第二拍
            NoteEvent(None, 0.5, 60),    # 第三拍
        ]
        
        pattern = RhythmPattern(
            name="Waltz",
            time_signature=time_signature,
            note_events=events,
            bpm=bpm,
            description="华尔兹节奏：强-弱-弱"
        )
        
        return pattern
    
    @staticmethod
    def create_funk(time_signature: TimeSignature = TimeSignature.FOUR_FOUR, bpm: int = 110) -> RhythmPattern:
        """放克节奏"""
        events = [
            NoteEvent(None, 1.0, 70),    # 底鼓
            NoteEvent(None, 0.5, 90),     # 军鼓
            NoteEvent(None, 0.5, 80),    # 底鼓
            NoteEvent(None, 0.5, 90),    # 军鼓
            NoteEvent(None, 0.5, 85),    # 底鼓
            NoteEvent(None, 0.5, 90),    # 军鼓
            NoteEvent(None, 0.5, 75),    # 底鼓
            NoteEvent(None, 0.5, 90),    # 军鼓
        ]
        
        pattern = RhythmPattern(
            name="Funk",
            time_signature=time_signature,
            note_events=events,
            bpm=bpm,
            description="放克节奏：切分音型"
        )
        
        return pattern
    
    @staticmethod
    def create_swing(time_signature: TimeSignature = TimeSignature.FOUR_FOUR, bpm: int = 140) -> RhythmPattern:
        """摇摆节奏（Swing 8th notes）"""
        events = [
            NoteEvent(None, 0.67, 80),   # 长音
            NoteEvent(None, 0.33, 60),   # 短音
            NoteEvent(None, 0.67, 80),   # 长音
            NoteEvent(None, 0.33, 60),   # 短音
            NoteEvent(None, 0.67, 80),   # 长音
            NoteEvent(None, 0.33, 60),   # 短音
            NoteEvent(None, 0.67, 80),   # 长音
            NoteEvent(None, 0.33, 60),   # 短音
        ]
        
        pattern = RhythmPattern(
            name="Swing",
            time_signature=time_signature,
            note_events=events,
            bpm=bpm,
            description="摇摆节奏：三连音式的八分音符"
        )
        
        return pattern
    
    @staticmethod
    def create_blues(time_signature: TimeSignature = TimeSignature.FOUR_FOUR, bpm: int = 80) -> RhythmPattern:
        """蓝调节奏"""
        events = [
            NoteEvent(None, 1.0, 80),    # 底鼓（第一拍）
            NoteEvent(None, 1.0, 70),    # 底鼓（第二拍）
            NoteEvent(None, 0.5, 90),   # 军鼓（第三拍前半）
            NoteEvent(None, 0.5, 80),   # 底鼓（第三拍后半）
            NoteEvent(None, 1.0, 70),   # 底鼓（第四拍）
        ]
        
        pattern = RhythmPattern(
            name="Blues",
            time_signature=time_signature,
            note_events=events,
            bpm=bpm,
            description="蓝调节奏：12小节进行基础"
        )
        
        return pattern


class RhythmAnalyzer:
    """节奏分析器"""
    
    @staticmethod
    def analyze_pattern(pattern: RhythmPattern) -> Dict[str, Any]:
        """分析节奏模式"""
        analysis = {
            "name": pattern.name,
            "time_signature": pattern.time_signature.value,
            "bpm": pattern.bpm,
            "total_beats": pattern.get_total_beats(),
            "total_measures": pattern.get_duration(),
            "note_count": len(pattern.note_events),
            "rhythmic_density": 0,
            "accents": [],
            "syncopation": 0,
            "complexity": "Simple"
        }
        
        # 分析节奏密度
        total_duration = pattern.get_total_beats()
        analysis["rhythmic_density"] = len(pattern.note_events) / total_duration if total_duration > 0 else 0
        
        # 分析重音和切分音
        current_beat = 0
        for event in pattern.note_events:
            beat_position = current_beat % pattern.time_signature.beats_per_measure
            
            # 检查重音
            if event.velocity > 90:
                analysis["accents"].append(beat_position + 1)
            
            # 检查切分音（在弱拍上演奏）
            if beat_position not in [0, 2] and event.velocity > 70:  # 假设4/4拍
                analysis["syncopation"] += 1
            
            current_beat += event.get_total_duration()
        
        # 计算切分音程度
        total_events = len(pattern.note_events)
        analysis["syncopation"] = (analysis["syncopation"] / total_events * 100) if total_events > 0 else 0
        
        # 评估复杂度
        if analysis["rhythmic_density"] > 8:
            analysis["complexity"] = "Complex"
        elif analysis["rhythmic_density"] > 4:
            analysis["complexity"] = "Medium"
        else:
            analysis["complexity"] = "Simple"
        
        return analysis
    
    @staticmethod
    def compare_patterns(pattern1: RhythmPattern, pattern2: RhythmPattern) -> Dict[str, Any]:
        """比较两个节奏模式"""
        comparison = {
            "similarity": 0,
            "differences": [],
            "rhythm_complexity_diff": 0
        }
        
        # 比较基本特征
        if pattern1.time_signature != pattern2.time_signature:
            comparison["differences"].append("拍号不同")
        
        if pattern1.bpm != pattern2.bpm:
            comparison["differences"].append(f"BPM不同: {pattern1.bpm} vs {pattern2.bpm}")
        
        # 分析节奏密度差异
        density1 = len(pattern1.note_events) / pattern1.get_total_beats()
        density2 = len(pattern2.note_events) / pattern2.get_total_beats()
        comparison["rhythm_complexity_diff"] = abs(density1 - density2)
        
        # 计算相似度（简化版）
        similarity_factors = []
        
        # BPM相似度
        bpm_diff = abs(pattern1.bpm - pattern2.bpm)
        if bpm_diff <= 10:
            similarity_factors.append(0.8)
        elif bpm_diff <= 20:
            similarity_factors.append(0.5)
        else:
            similarity_factors.append(0.1)
        
        # 节奏密度相似度
        density_diff = abs(density1 - density2)
        if density_diff <= 0.5:
            similarity_factors.append(0.7)
        elif density_diff <= 1.0:
            similarity_factors.append(0.4)
        else:
            similarity_factors.append(0.1)
        
        # 拍号相似度
        if pattern1.time_signature == pattern2.time_signature:
            similarity_factors.append(0.9)
        else:
            similarity_factors.append(0.3)
        
        # 综合相似度
        comparison["similarity"] = sum(similarity_factors) / len(similarity_factors)
        
        return comparison


# 预定义常用节奏模式
COMMON_RHYTHMS = {
    "rock_beat": RhythmFactory.create_rock_beat(),
    "waltz": RhythmFactory.create_waltz(),
    "funk": RhythmFactory.create_funk(),
    "swing": RhythmFactory.create_swing(),
    "blues": RhythmFactory.create_blues(),
    "rock_fast": RhythmFactory.create_rock_beat(bpm=160),
    "ballad": RhythmFactory.create_waltz(bpm=80),
    "disco": RhythmFactory.create_funk(bpm=120),
}