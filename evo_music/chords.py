"""
和弦系统 - 各种和弦的创建和分析
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .notes import NoteName


class ChordType:
    """和弦类型常量"""
    # 三和弦
    MAJOR = "major"           # 大三和弦
    MINOR = "minor"           # 小三和弦
    AUGMENTED = "augmented"   # 增三和弦
    DIMINISHED = "diminished" # 减三和弦
    
    # 七和弦
    MAJOR7 = "major7"         # 大七和弦
    MINOR7 = "minor7"         # 小七和弦
    DOMINANT7 = "dominant7"   # 属七和弦
    AUGMENTED7 = "augmented7" # 增七和弦
    DIMINISHED7 = "diminished7" # 减七和弦
    HALF_DIMINISHED7 = "half_diminished7" # 半减七和弦
    
    # 九和弦
    MAJOR9 = "major9"         # 大九和弦
    MINOR9 = "minor9"         # 小九和弦
    DOMINANT9 = "dominant9"   # 属九和弦
    MAJOR9_flat5 = "major9_flat5"  # 大九和弦减五度
    MINOR9_flat5 = "minor9_flat5"  # 小九和弦减五度
    
    # 十一和弦
    MAJOR11 = "major11"       # 大十一和弦
    MINOR11 = "minor11"       # 小十一和弦
    DOMINANT11 = "dominant11" # 属十一和弦
    
    # 十三和弦
    MAJOR13 = "major13"       # 大十三和弦
    MINOR13 = "minor13"       # 小十三和弦
    DOMINANT13 = "dominant13" # 属十三和弦


@dataclass
class Chord:
    """和弦数据结构"""
    name: str                    # 和弦名称（如："C Major"）
    chord_type: str              # 和弦类型
    root_note: NoteName          # 根音
    bass_note: Optional[NoteName] # 低音（用于转位）
    notes: List[NoteName]        # 构成音
    extensions: List[int]        # 扩展音（9th, 11th, 13th）
    description: str             # 和弦描述
    function: Optional[str]      # 功能标记（如：I, ii, iii, IV, V, vi, vii°）
    
    def __post_init__(self):
        """数据初始化后的处理"""
        if not self.notes:
            # 如果没有音符列表，根据和弦类型计算
            self.notes = self._calculate_notes()
    
    def _calculate_notes(self) -> List[NoteName]:
        """根据和弦类型计算构成音"""
        intervals = CHORD_INTERVALS.get(self.chord_type, [0, 4, 7])
        notes = []
        
        for interval in intervals:
            note = self.root_note.value + interval
            notes.append(NoteName(note % 12))
        
        return notes
    
    def get_note_at_position(self, position: int) -> Optional[NoteName]:
        """获取和弦中指定位置的音"""
        if 0 <= position < len(self.notes):
            return self.notes[position]
        return None
    
    def is_triad(self) -> bool:
        """是否为三和弦"""
        return len(self.notes) == 3
    
    def is_seventh_chord(self) -> bool:
        """是否为七和弦"""
        return 7 in [self.root_note.value + 7] or self._contains_extension(7)
    
    def is_ninth_chord(self) -> bool:
        """是否为九和弦"""
        return self._contains_extension(9)
    
    def is_eleventh_chord(self) -> bool:
        """是否为十一和弦"""
        return self._contains_extension(11)
    
    def is_thirteenth_chord(self) -> bool:
        """是否为十三和弦"""
        return self._contains_extension(13)
    
    def _contains_extension(self, extension: int) -> bool:
        """检查是否包含指定的扩展音"""
        base_intervals = CHORD_INTERVALS.get(self.chord_type, [0, 4, 7])
        return any(interval == extension for interval in base_intervals) or extension in self.extensions
    
    def get_inversions(self) -> List['Chord']:
        """获取和弦的转位"""
        inversions = []
        
        for i in range(1, len(self.notes)):
            # 创建转位和弦
            inverted_notes = self.notes[i:] + self.notes[:i]
            
            # 确定低音
            bass_note = inverted_notes[0]
            
            # 创建转位和弦
            inverted_chord = Chord(
                name=f"{self.root_note.value_str}/{bass_note.value_str}",
                chord_type=self.chord_type,
                root_note=self.root_note,
                bass_note=bass_note,
                notes=inverted_notes,
                extensions=self.extensions,
                description=f"{self.name} 第{i}转位",
                function=self.function
            )
            
            inversions.append(inverted_chord)
        
        return inversions
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "chord_type": self.chord_type,
            "root_note": self.root_note.value_str,
            "bass_note": self.bass_note.value_str if self.bass_note else None,
            "notes": [note.value_str for note in self.notes],
            "extensions": self.extensions,
            "description": self.description,
            "function": self.function,
            "is_triad": self.is_triad(),
            "is_seventh": self.is_seventh_chord(),
            "is_ninth": self.is_ninth_chord(),
            "is_eleventh": self.is_eleventh_chord(),
            "is_thirteenth": self.is_thirteenth_chord()
        }


# 和弦模式定义（相对于根音的半音数）
CHORD_INTERVALS = {
    # 三和弦
    ChordType.MAJOR: [0, 4, 7],                     # 大三和弦
    ChordType.MINOR: [0, 3, 7],                     # 小三和弦
    ChordType.AUGMENTED: [0, 4, 8],                 # 增三和弦
    ChordType.DIMINISHED: [0, 3, 6],                # 减三和弦
    
    # 七和弦
    ChordType.MAJOR7: [0, 4, 7, 11],               # 大七和弦
    ChordType.MINOR7: [0, 3, 7, 10],               # 小七和弦
    ChordType.DOMINANT7: [0, 4, 7, 10],            # 属七和弦
    ChordType.AUGMENTED7: [0, 4, 8, 10],           # 增七和弦
    ChordType.DIMINISHED7: [0, 3, 6, 9],           # 减七和弦
    ChordType.HALF_DIMINISHED7: [0, 3, 6, 10],     # 半减七和弦
    
    # 九和弦
    ChordType.MAJOR9: [0, 4, 7, 11, 14],          # 大九和弦
    ChordType.MINOR9: [0, 3, 7, 10, 14],          # 小九和弦
    ChordType.DOMINANT9: [0, 4, 7, 10, 14],       # 属九和弦
    ChordType.MAJOR9_flat5: [0, 4, 6, 11, 14],    # 大九和弦减五度
    ChordType.MINOR9_flat5: [0, 3, 6, 10, 14],    # 小九和弦减五度
    
    # 十一和弦
    ChordType.MAJOR11: [0, 4, 7, 11, 14, 17],      # 大十一和弦
    ChordType.MINOR11: [0, 3, 7, 10, 14, 17],     # 小十一和弦
    ChordType.DOMINANT11: [0, 4, 7, 10, 14, 17],  # 属十一和弦
    
    # 十三和弦
    ChordType.MAJOR13: [0, 4, 7, 11, 14, 17, 21], # 大十三和弦
    ChordType.MINOR13: [0, 3, 7, 10, 14, 17, 21], # 小十三和弦
    ChordType.DOMINANT13: [0, 4, 7, 10, 14, 17, 21], # 属十三和弦
}


class ChordFactory:
    """和弦工厂类"""
    
    @staticmethod
    def create_chord(root_note: NoteName, chord_type: str, extensions: List[int] = None) -> Chord:
        """创建指定类型的和弦"""
        if extensions is None:
            extensions = []
        
        chord = Chord(
            name=f"{root_note.value_str} {chord_type.replace('_', ' ').title()}",
            chord_type=chord_type,
            root_note=root_note,
            bass_note=None,
            notes=[],
            extensions=extensions,
            description=f"{chord_type.replace('_', ' ')}和弦",
            function=None
        )
        
        return chord
    
    @staticmethod
    def create_triad(root_note: NoteName, chord_type: str = ChordType.MAJOR) -> Chord:
        """创建三和弦"""
        return ChordFactory.create_chord(root_note, chord_type)
    
    @staticmethod
    def create_seventh_chord(root_note: NoteName, chord_type: str = ChordType.MAJOR7) -> Chord:
        """创建七和弦"""
        return ChordFactory.create_chord(root_note, chord_type)
    
    @staticmethod
    def create_ninth_chord(root_note: NoteName, chord_type: str = ChordType.MAJOR9) -> Chord:
        """创建九和弦"""
        return ChordFactory.create_chord(root_note, chord_type)
    
    @staticmethod
    def create_eleventh_chord(root_note: NoteName, chord_type: str = ChordType.MAJOR11) -> Chord:
        """创建十一和弦"""
        return ChordFactory.create_chord(root_note, chord_type)
    
    @staticmethod
    def create_thirteenth_chord(root_note: NoteName, chord_type: str = ChordType.MAJOR13) -> Chord:
        """创建十三和弦"""
        return ChordFactory.create_chord(root_note, chord_type)


class ChordProgressionAnalyzer:
    """和弦进行分析器"""
    
    @staticmethod
    def analyze_progression(chords: List[Chord]) -> Dict[str, Any]:
        """分析和弦进行"""
        analysis = {
            "length": len(chords),
            "key_changes": [],
            "common_progressions": [],
            "tension_level": 0,
            "chord_types": {},
            "root_movement": [],
            "functions": []
        }
        
        # 统计和弦类型
        for chord in chords:
            if chord.chord_type not in analysis["chord_types"]:
                analysis["chord_types"][chord.chord_type] = 0
            analysis["chord_types"][chord.chord_type] += 1
        
        # 分析根音运动
        for i in range(len(chords) - 1):
            current = chords[i]
            next_chord = chords[i + 1]
            movement = (next_chord.root_note.value - current.root_note.value) % 12
            analysis["root_movement"].append(movement)
        
        # 分析功能标记
        for chord in chords:
            if chord.function:
                analysis["functions"].append(chord.function)
        
        # 识别常见和弦进行
        common_patterns = [
            ["I", "IV", "V", "I"],      # 1-4-5-1
            ["vi", "IV", "I", "V"],      # 6-4-1-5
            ["ii", "V", "I"],            # 2-5-1
            ["I", "V", "vi", "IV"],      # 1-5-6-4 (流行音乐常用)
            ["I", "vi", "IV", "V"],      # 1-6-4-5 (经典流行)
        ]
        
        analysis["common_progressions"] = common_patterns
        
        # 计算紧张度
        seventh_chords = sum(1 for chord in chords if chord.is_seventh_chord())
        tension_level = (seventh_chords / len(chords)) * 100 if chords else 0
        analysis["tension_level"] = min(tension_level, 100)
        
        return analysis
    
    @staticmethod
    def find_related_chords(chord: Chord, key_scale: 'Scale') -> List[Chord]:
        """根据调性查找相关和弦"""
        related = []
        
        # 根据调性的音阶创建和弦
        for i, note in enumerate(key_scale.notes):
            chord_types = ["triad"]
            if i == 4:  # 属音
                chord_types.append("dominant7")
            elif i == 0 or i == 3:  # 主音和下属音
                chord_types.append("major7")
            elif i == 2 or i == 5 or i == 6:  # 中音、下中和音、导音
                chord_types.append("minor7")
            
            for chord_type in chord_types:
                if chord_type == "triad":
                    if i == 0 or i == 3 or i == 4:
                        c = ChordFactory.create_triad(note, ChordType.MAJOR)
                    elif i == 1 or i == 6:
                        c = ChordFactory.create_triad(note, ChordType.DIMINISHED)
                    else:
                        c = ChordFactory.create_triad(note, ChordType.MINOR)
                elif chord_type == "major7":
                    c = ChordFactory.create_seventh_chord(note, ChordType.MAJOR7)
                elif chord_type == "minor7":
                    c = ChordFactory.create_seventh_chord(note, ChordType.MINOR7)
                elif chord_type == "dominant7":
                    c = ChordFactory.create_seventh_chord(note, ChordType.DOMINANT7)
                
                # 设置功能标记
                roman_numerals = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
                c.function = roman_numerals[i]
                
                related.append(c)
        
        return related


class ChordUtils:
    """和弦工具类"""
    
    @staticmethod
    def get_enharmonic_equivalents(chord: Chord) -> List[str]:
        """获取等音和弦名称"""
        equivalents = []
        
        # 等音替换
        enharmonic_map = {
            "C#": ["Db"],
            "Db": ["C#"],
            "D#": ["Eb"],
            "Eb": ["D#"],
            "F#": ["Gb"],
            "Gb": ["F#"],
            "G#": ["Ab"],
            "Ab": ["G#"],
            "A#": ["Bb"],
            "Bb": ["A#"]
        }
        
        root_str = chord.root_note.value_str
        if root_str in enharmonic_map:
            for equiv in enharmonic_map[root_str]:
                equivalents.append(f"{equiv} {chord.chord_type}")
        
        return equivalents
    
    @staticmethod
    def simplify_chord_name(chord_name: str) -> str:
        """简化和弦名称"""
        # 移除重复的信息
        simplified = chord_name.replace("Major", "").replace("minor", "m")
        simplified = simplified.replace("7th", "7")
        simplified = simplified.replace("9th", "9")
        simplified = simplified.replace("11th", "11")
        simplified = simplified.replace("13th", "13")
        
        return simplified
    
    @staticmethod
    def get_chord_formula(chord_type: str) -> str:
        """获取和弦公式"""
        formulas = {
            ChordType.MAJOR: "1-3-5",
            ChordType.MINOR: "1-♭3-5",
            ChordType.AUGMENTED: "1-3-♯5",
            ChordType.DIMINISHED: "1-♭3-♭5",
            ChordType.MAJOR7: "1-3-5-7",
            ChordType.MINOR7: "1-♭3-5-♭7",
            ChordType.DOMINANT7: "1-3-5-♭7",
            ChordType.HALF_DIMINISHED7: "1-♭3-♭5-♭7",
            ChordType.DIMINISHED7: "1-♭3-♭5-♭♭7",
        }
        
        return formulas.get(chord_type, "Unknown")


# 预定义常用和弦
PREDEFINED_CHORDS = {
    # 大调和弦
    "C_major": ChordFactory.create_triad(NoteName.C, ChordType.MAJOR),
    "G_major": ChordFactory.create_triad(NoteName.G, ChordType.MAJOR),
    "D_major": ChordFactory.create_triad(NoteName(NoteName.C.value + 2), ChordType.MAJOR),  # D
    "A_major": ChordFactory.create_triad(NoteName(NoteName.C.value + 3), ChordType.MAJOR),  # A
    "E_major": ChordFactory.create_triad(NoteName(NoteName.C.value + 4), ChordType.MAJOR),  # E
    "B_major": ChordFactory.create_triad(NoteName(NoteName.C.value + 5), ChordType.MAJOR),  # B
    "F_major": ChordFactory.create_triad(NoteName(NoteName.C.value + 5), ChordType.MAJOR),   # F (B-1)
    
    # 小调和弦
    "A_minor": ChordFactory.create_triad(NoteName(NoteName.C.value + 9), ChordType.MINOR),  # Am
    "E_minor": ChordFactory.create_triad(NoteName(NoteName.C.value + 4), ChordType.MINOR),  # Em
    "D_minor": ChordFactory.create_triad(NoteName(NoteName.C.value + 2), ChordType.MINOR),  # Dm
    "B_minor": ChordFactory.create_triad(NoteName(NoteName.C.value + 11), ChordType.MINOR), # Bm
    "F_minor": ChordFactory.create_triad(NoteName(NoteName.C.value + 5), ChordType.MINOR),  # Fm
    
    # 七和弦
    "C_major7": ChordFactory.create_seventh_chord(NoteName.C, ChordType.MAJOR7),
    "G_major7": ChordFactory.create_seventh_chord(NoteName.G, ChordType.MAJOR7),
    "D_minor7": ChordFactory.create_seventh_chord(NoteName(NoteName.C.value + 2), ChordType.MINOR7),  # Dm7
    "E_minor7": ChordFactory.create_seventh_chord(NoteName(NoteName.C.value + 4), ChordType.MINOR7),  # Em7
    "A_minor7": ChordFactory.create_seventh_chord(NoteName(NoteName.C.value + 9), ChordType.MINOR7), # Am7
    "Dominant7": ChordFactory.create_seventh_chord(NoteName(NoteName.C.value + 7), ChordType.DOMINANT7),  # G7
    
    # 转位和弦
    "C_first_inversion": ChordFactory.create_triad(NoteName.C, ChordType.MAJOR).get_inversions()[0] if ChordFactory.create_triad(NoteName.C, ChordType.MAJOR).get_inversions() else None,
}