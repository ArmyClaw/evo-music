"""
音阶系统 - 各种音阶的创建和分析
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .notes import NoteName, SCALE_INTERVALS, get_note_from_interval


class ScaleType:
    """音阶类型常量"""
    # 基础大小调
    MAJOR = "major"
    NATURAL_MINOR = "natural_minor"
    HARMONIC_MINOR = "harmonic_minor"
    MELODIC_MINOR = "melodic_minor"
    
    # 五声音阶
    PENTATONIC_MAJOR = "pentatonic_major"
    PENTATONIC_MINOR = "pentatonic_minor"
    CHINESE_MAJOR = "chinese_major"    # 中国五声（宫商角徵羽）
    JAPANESE = "japanese"              # 日本音阶
    
    # 布鲁斯音阶
    BLUES_MAJOR = "blues_major"
    BLUES_MINOR = "blues_minor"
    
    # 教会调式
    DORIAN = "dorian"
    PHRYGIAN = "phrygian"
    LYDIAN = "lydian"
    MIXOLYDIAN = "mixolydian"
    LOCRIAN = "locrian"
    
    # 现代音阶
    WHOLE_TONE = "whole_tone"           # 全音音阶
    CHROMATIC = "chromatic"             # 半音音阶
    AUGMENTED = "augmented"             # 增三和弦音阶
    DIMINISHED = "diminished"           # 减七和弦音阶
    
    # 其他民族音阶
    HINDUSTANI = "hindustani"           # 印度音阶
    FLAMENCO = "flamenco"               # 弗拉明戈音阶
    GYPSY = "gypsy"                     # 吉普赛音阶


@dataclass
class Scale:
    """音阶数据结构"""
    name: str                    # 音阶名称（如："C Major"）
    scale_type: str              # 音阶类型
    root_note: NoteName          # 根音
    intervals: List[int]         # 音程模式（相对于根音的半音数）
    notes: List[NoteName]        # 构成音
    description: str             # 音阶描述
    
    def generate_sequence(self, length: int, direction: str = "up", octave_range: int = 2) -> List[NoteName]:
        """生成音阶序列
        
        Args:
            length: 序列长度
            direction: 方向 ("up", "down", "up_down")
            octave_range: 音程范围（几个八度）
            
        Returns:
            音符序列
        """
        sequence = []
        
        if direction == "up":
            # 向上生成序列
            for octave in range(octave_range + 1):
                for interval in self.intervals:
                    if len(sequence) >= length:
                        break
                    note_value = (self.root_note.value + interval + octave * 12) % 12
                    sequence.append(NoteName(note_value))
                if len(sequence) >= length:
                    break
                    
        elif direction == "down":
            # 向下生成序列
            for octave in range(octave_range, -1, -1):
                for interval in reversed(self.intervals):
                    if len(sequence) >= length:
                        break
                    note_value = (self.root_note.value + interval + octave * 12) % 12
                    sequence.append(NoteName(note_value))
                if len(sequence) >= length:
                    break
                    
        elif direction == "up_down":
            # 上下往返生成序列
            # 向上行
            for octave in range(octave_range + 1):
                for interval in self.intervals:
                    if len(sequence) >= length:
                        break
                    note_value = (self.root_note.value + interval + octave * 12) % 12
                    sequence.append(NoteName(note_value))
                if len(sequence) >= length:
                    break
            
            # 向下回（跳过重复的根音）
            if len(sequence) < length:
                for octave in range(octave_range - 1, -1, -1):
                    for interval in reversed(self.intervals[1:]):  # 跳过根音避免重复
                        if len(sequence) >= length:
                            break
                        note_value = (self.root_note.value + interval + octave * 12) % 12
                        sequence.append(NoteName(note_value))
                    if len(sequence) >= length:
                        break
        
        return sequence[:length]
    
    def get_scale_degrees(self) -> Dict[str, NoteName]:
        """获取音阶的音级名称
        
        Returns:
            {音级名称: 音符}
        """
        degree_names = {
            ScaleType.MAJOR: ["I", "II", "III", "IV", "V", "VI", "VII"],
            ScaleType.NATURAL_MINOR: ["i", "ii", "III", "iv", "v", "VI", "VII"],
            ScaleType.HARMONIC_MINOR: ["i", "ii", "III+", "iv", "V", "VI", "vii°"],
            ScaleType.PENTATONIC_MAJOR: ["I", "II", "III", "V", "VI"],
            ScaleType.PENTATONIC_MINOR: ["i", "ii", "iv", "v", "vi"],
        }
        
        names = degree_names.get(self.scale_type, ["I", "II", "III", "IV", "V", "VI", "VII"])
        return {name: note for name, note in zip(names, self.notes)}
    
    def __post_init__(self):
        """数据初始化后的处理"""
        if not self.notes and self.intervals:
            # 如果没有音符列表，根据音程模式计算
            self.notes = []
            for interval in self.intervals:
                note = get_note_from_interval(self.root_note, interval)
                self.notes.append(note)
    
    def get_note_at_position(self, position: int) -> Optional[NoteName]:
        """获取音阶中指定位置的音"""
        if 0 <= position < len(self.notes):
            return self.notes[position]
        return None
    
    def get_chord_recommendations(self) -> List[str]:
        """获取该音阶常用的和弦推荐"""
        # 根据音阶类型返回推荐和弦
        chord_rec = {
            # 基础大小调
            ScaleType.MAJOR: ["I", "ii", "iii", "IV", "V", "vi", "vii°"],
            ScaleType.NATURAL_MINOR: ["i", "ii°", "III", "iv", "v", "VI", "VII"],
            ScaleType.HARMONIC_MINOR: ["i", "ii°", "III+", "iv", "V", "VI", "vii°"],
            ScaleType.MELODIC_MINOR: ["i", "ii°", "III+", "IV", "V", "vi°", "vii°"],
            
            # 五声音阶
            ScaleType.PENTATONIC_MAJOR: ["I", "ii", "IV", "V"],
            ScaleType.PENTATONIC_MINOR: ["i", "iv", "v"],
            ScaleType.CHINESE_MAJOR: ["I", "ii", "iii", "V", "vi"],
            ScaleType.JAPANESE: ["i", "ii", "IV", "V"],
            
            # 布鲁斯音阶
            ScaleType.BLUES_MAJOR: ["I", "IV", "V", "I7", "IV7", "V7"],
            ScaleType.BLUES_MINOR: ["i", "iv", "V", "i7", "iv7", "V7", "I7"],
            
            # 教会调式
            ScaleType.DORIAN: ["i", "ii", "IV", "v", "vi°", "VII"],
            ScaleType.PHRYGIAN: ["i", "II", "iv", "v", "VI", "vii°"],
            ScaleType.LYDIAN: ["I", "ii", "iii", "iv°", "V", "vi"],
            ScaleType.MIXOLYDIAN: ["I", "ii", "iii", "IV", "v", "vi"],
            ScaleType.LOCRIAN: ["i", "ii°", "III", "iv", "V", "VI", "vii"],
            
            # 现代音阶
            ScaleType.WHOLE_TONE: ["I", "ii", "iii", "IV", "V", "vi"],
            ScaleType.CHROMATIC: ["所有和弦"],
            ScaleType.AUGMENTED: ["I", "III", "V"],
            ScaleType.DIMINISHED: ["i", "iii", "v", "vii"],
            
            # 民族音阶
            ScaleType.HINDUSTANI: ["I", "II", "IV", "V", "VI", "vii"],
            ScaleType.FLAMENCO: ["i", "II", "III", "IV", "V", "vii"],
            ScaleType.GYPSY: ["i", "II", "IV", "V", "vii"],
        }
        
        return chord_rec.get(self.scale_type, ["常用和弦"])
    
    def get_relative_key(self) -> Optional['Scale']:
        """获取关系大小调"""
        if self.scale_type == ScaleType.MAJOR:
            # 大调的关系小调是下方小三度
            minor_intervals = SCALE_INTERVALS[ScaleType.NATURAL_MINOR]
            root_note = get_note_from_interval(self.root_note, -3)
            return Scale(
                name=f"{root_note.value_str} Natural Minor",
                scale_type=ScaleType.NATURAL_MINOR,
                root_note=root_note,
                intervals=minor_intervals,
                notes=[],
                description=f"{self.name}的关系小调"
            )
        elif self.scale_type == ScaleType.NATURAL_MINOR:
            # 小调的关系大调是上方大三度
            major_intervals = SCALE_INTERVALS[ScaleType.MAJOR]
            root_note = get_note_from_interval(self.root_note, 3)
            return Scale(
                name=f"{root_note.value_str} Major",
                scale_type=ScaleType.MAJOR,
                root_note=root_note,
                intervals=major_intervals,
                notes=[],
                description=f"{self.name}的关系大调"
            )
        return None
    
    def get_parallel_minor(self) -> Optional['Scale']:
        """获取平行小调"""
        if self.scale_type == ScaleType.MAJOR:
            minor_intervals = SCALE_INTERVALS[ScaleType.NATURAL_MINOR]
            return Scale(
                name=f"{self.root_note.value_str} Natural Minor",
                scale_type=ScaleType.NATURAL_MINOR,
                root_note=self.root_note,
                intervals=minor_intervals,
                notes=[],
                description=f"{self.name}的平行小调"
            )
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "scale_type": self.scale_type,
            "root_note": self.root_note.value_str,
            "intervals": self.intervals,
            "notes": [note.value_str for note in self.notes],
            "description": self.description,
            "chord_recommendations": self.get_chord_recommendations()
        }


class ScaleFactory:
    """音阶工厂类，用于创建各种音阶"""
    
    @staticmethod
    def create_scale(root_note: NoteName, scale_type: str = ScaleType.MAJOR) -> Scale:
        """创建指定类型的音阶"""
        intervals = SCALE_INTERVALS.get(scale_type, SCALE_INTERVALS[ScaleType.MAJOR])
        
        scale = Scale(
            name=f"{root_note.value_str} {scale_type.replace('_', ' ').title()}",
            scale_type=scale_type,
            root_note=root_note,
            intervals=intervals,
            notes=[],
            description=f"{scale_type.replace('_', ' ')}音阶"
        )
        
        return scale
    
    @staticmethod
    def create_major_scale(root_note: NoteName) -> Scale:
        """创建大调音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.MAJOR)
    
    @staticmethod
    def create_minor_scale(root_note: NoteName, minor_type: str = "natural") -> Scale:
        """创建小调音阶"""
        scale_type_map = {
            "natural": ScaleType.NATURAL_MINOR,
            "harmonic": ScaleType.HARMONIC_MINOR,
            "melodic": ScaleType.MELODIC_MINOR,
        }
        
        scale_type = scale_type_map.get(minor_type, ScaleType.NATURAL_MINOR)
        return ScaleFactory.create_scale(root_note, scale_type)
    
    @staticmethod
    def create_pentatonic_scale(root_note: NoteName, scale_type: str = "major") -> Scale:
        """创建五声音阶"""
        scale_type_map = {
            "major": ScaleType.PENTATONIC_MAJOR,
            "minor": ScaleType.PENTATONIC_MINOR,
        }
        
        actual_type = scale_type_map.get(scale_type, ScaleType.PENTATONIC_MAJOR)
        return ScaleFactory.create_scale(root_note, actual_type)
    
    @staticmethod
    def create_blues_scale(root_note: NoteName, scale_type: str = "major") -> Scale:
        """创建布鲁斯音阶"""
        scale_type_map = {
            "major": ScaleType.BLUES_MAJOR,
            "minor": ScaleType.BLUES_MINOR,
        }
        
        actual_type = scale_type_map.get(scale_type, ScaleType.BLUES_MAJOR)
        return ScaleFactory.create_scale(root_note, actual_type)
    
    @staticmethod
    def create_mode_scale(root_note: NoteName, mode: str) -> Scale:
        """创建教会调式音阶"""
        mode_map = {
            "ionian": ScaleType.MAJOR,           # 同大调
            "dorian": ScaleType.DORIAN,         # 多利亚
            "phrygian": ScaleType.PHRYGIAN,     # 弗里几亚
            "lydian": ScaleType.LYDIAN,         # 利底亚
            "mixolydian": ScaleType.MIXOLYDIAN, # 混合利底亚
            "aeolian": ScaleType.NATURAL_MINOR,  # 同自然小调
            "locrian": ScaleType.LOCRIAN,       # 洛克里亚
        }
        
        actual_type = mode_map.get(mode.lower(), ScaleType.MAJOR)
        return ScaleFactory.create_scale(root_note, actual_type)
    
    @staticmethod
    def create_chinese_scale(root_note: NoteName) -> Scale:
        """创建中国五声音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.CHINESE_MAJOR)
    
    @staticmethod
    def create_japanese_scale(root_note: NoteName) -> Scale:
        """创建日本音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.JAPANESE)
    
    @staticmethod
    def create_whole_tone_scale(root_note: NoteName) -> Scale:
        """创建全音音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.WHOLE_TONE)
    
    @staticmethod
    def create_chromatic_scale(root_note: NoteName) -> Scale:
        """创建半音音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.CHROMATIC)
    
    @staticmethod
    def create_augmented_scale(root_note: NoteName) -> Scale:
        """创建增三和弦音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.AUGMENTED)
    
    @staticmethod
    def create_diminished_scale(root_note: NoteName) -> Scale:
        """创建减七和弦音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.DIMINISHED)
    
    @staticmethod
    def create_hindustani_scale(root_note: NoteName) -> Scale:
        """创建印度音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.HINDUSTANI)
    
    @staticmethod
    def create_flamenco_scale(root_note: NoteName) -> Scale:
        """创建弗拉明戈音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.FLAMENCO)
    
    @staticmethod
    def create_gypsy_scale(root_note: NoteName) -> Scale:
        """创建吉普赛音阶"""
        return ScaleFactory.create_scale(root_note, ScaleType.GYPSY)


class ScaleAnalyzer:
    """音阶分析器"""
    
    @staticmethod
    def analyze_scale(scale: Scale) -> Dict[str, Any]:
        """分析音阶特征"""
        analysis = {
            "name": scale.name,
            "type": scale.scale_type,
            "root": scale.root_note.value_str,
            "notes_count": len(scale.notes),
            "has_semitone_intervals": False,
            "interval_pattern": [],
            "characteristics": [],
        }
        
        # 分析音程模式
        for i in range(len(scale.intervals) - 1):
            interval = scale.intervals[i + 1] - scale.intervals[i]
            analysis["interval_pattern"].append(interval)
            if interval == 1:  # 半音
                analysis["has_semitone_intervals"] = True
        
        # 分析音阶特征
        if scale.scale_type == ScaleType.MAJOR:
            analysis["characteristics"] = ["明亮", "稳定", "常用"]
        elif scale.scale_type == ScaleType.NATURAL_MINOR:
            analysis["characteristics"] = ["忧郁", "自然", "古典"]
        elif scale.scale_type == ScaleType.HARMONIC_MINOR:
            analysis["characteristics"] = ["戏剧性", "异域风情", "导音强烈"]
        elif scale.scale_type == ScaleType.PENTATONIC_MAJOR:
            analysis["characteristics"] = ["柔和", "东方", "简单"]
        elif scale.scale_type == ScaleType.BLUES_MINOR:
            analysis["characteristics"] = ["蓝调", "忧郁", "摇摆"]
        
        return analysis
    
    @staticmethod
    def find_scales_with_note(note: NoteName) -> List[Scale]:
        """查找包含指定音符的音阶"""
        scales = []
        note_str = note.value_str
        
        # 创建12个调的所有主要音阶
        for root_note in NoteName:
            for scale_type in [ScaleType.MAJOR, ScaleType.NATURAL_MINOR, 
                              ScaleType.PENTATONIC_MAJOR, ScaleType.PENTATONIC_MINOR]:
                scale = ScaleFactory.create_scale(root_note, scale_type)
                if note_str in [n.value_str for n in scale.notes]:
                    scales.append(scale)
        
        return scales
    
    @staticmethod
    def compare_scales(scale1: Scale, scale2: Scale) -> Dict[str, Any]:
        """比较两个音阶的异同"""
        comparison = {
            "similarity": 0,
            "common_notes": [],
            "different_notes": [],
            "interval_differences": []
        }
        
        # 找到相同的音符
        notes1 = set(n.value_str for n in scale1.notes)
        notes2 = set(n.value_str for n in scale2.notes)
        
        comparison["common_notes"] = list(notes1.intersection(notes2))
        comparison["different_notes"] = {
            "scale1_only": list(notes1 - notes2),
            "scale2_only": list(notes2 - notes1)
        }
        
        # 比较音程模式
        if len(scale1.intervals) == len(scale2.intervals):
            comparison["interval_differences"] = [
                abs(scale1.intervals[i] - scale2.intervals[i]) 
                for i in range(len(scale1.intervals))
            ]
        
        # 计算相似度
        total_notes = len(notes1.union(notes2))
        comparison["similarity"] = len(comparison["common_notes"]) / total_notes if total_notes > 0 else 0
        
        return comparison


# 预定义常用音阶
PREDEFINED_SCALES = {
    "C_major": ScaleFactory.create_major_scale(NoteName.C),
    "A_minor": ScaleFactory.create_minor_scale(NoteName.A),
    "G_major": ScaleFactory.create_major_scale(NoteName.G),
    "E_minor": ScaleFactory.create_minor_scale(NoteName.E),
    "D_major": ScaleFactory.create_major_scale(NoteName.D),
    "B_minor": ScaleFactory.create_minor_scale(NoteName.B),
    "A_major": ScaleFactory.create_major_scale(NoteName.A),
    "F_minor": ScaleFactory.create_minor_scale(NoteName.F),
    "E_major": ScaleFactory.create_major_scale(NoteName.E),
    "C_minor": ScaleFactory.create_minor_scale(NoteName.C),
    "D_minor": ScaleFactory.create_minor_scale(NoteName.D),
    "B_flat_major": ScaleFactory.create_major_scale(NoteName(NoteName.C.value + 1)),  # Bb
    "F_major": ScaleFactory.create_major_scale(NoteName(NoteName.E.value + 1)),       # F
    "C_pentatonic_major": ScaleFactory.create_pentatonic_scale(NoteName.C),
    "A_pentatonic_minor": ScaleFactory.create_pentatonic_scale(NoteName.A, "minor"),
    "C_blues": ScaleFactory.create_blues_scale(NoteName.C),
    "A_blues": ScaleFactory.create_blues_scale(NoteName.A, "minor"),
}