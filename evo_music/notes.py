"""
音符和音程基础数据结构
"""

from enum import Enum
from typing import List


class NoteName(Enum):
    """音符名称枚举"""
    C = 0
    C_SHARP = 1
    D = 2
    D_SHARP = 3
    E = 4
    F = 5
    F_SHARP = 6
    G = 7
    G_SHARP = 8
    A = 9
    A_SHARP = 10
    B = 11
    
    @property
    def value_str(self) -> str:
        """返回音符字符串表示"""
        sharp_mapping = {
            1: "C#",
            3: "D#", 
            6: "F#",
            8: "G#",
            10: "A#"
        }
        if self.value in sharp_mapping:
            return sharp_mapping[self.value]
        else:
            return self.name
    
    @classmethod
    def from_string(cls, note_str: str) -> 'NoteName':
        """从字符串创建音符枚举"""
        mapping = {
            "C": cls.C,
            "C#": cls.C_SHARP, "Db": cls.C_SHARP,
            "D": cls.D,
            "D#": cls.D_SHARP, "Eb": cls.D_SHARP,
            "E": cls.E,
            "F": cls.F,
            "F#": cls.F_SHARP, "Gb": cls.F_SHARP,
            "G": cls.G,
            "G#": cls.G_SHARP, "Ab": cls.G_SHARP,
            "A": cls.A,
            "A#": cls.A_SHARP, "Bb": cls.A_SHARP,
            "B": cls.B
        }
        return mapping.get(note_str.upper(), cls.C)


class IntervalType(Enum):
    """音程类型枚举"""
    UNISON = 0          # 纯一度
    MINOR_SECOND = 1    # 小二度
    MAJOR_SECOND = 2    # 大二度
    MINOR_THIRD = 3     # 小三度
    MAJOR_THIRD = 4     # 大三度
    PERFECT_FOURTH = 5  # 纯四度
    AUGMENTED_FOURTH = 6 # 增四度
    DIMINISHED_FIFTH = 7 # 减五度
    PERFECT_FIFTH = 8   # 纯五度
    MINOR_SIXTH = 9     # 小六度
    MAJOR_SIXTH = 10    # 大六度
    MINOR_SEVENTH = 11  # 小七度
    MAJOR_SEVENTH = 12  # 大七度
    OCTAVE = 12         # 八度


# 常用音程模式（半音数）
SCALE_INTERVALS = {
    # 基础大小调
    # 大调音阶：全全半全全半全
    "major": [0, 2, 4, 5, 7, 9, 11],
    # 自然小调：全半全全半全全  
    "natural_minor": [0, 2, 3, 5, 7, 8, 10],
    # 和声小调：全半全全半增二度全
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    # 旋律小调（上行）：全半全全全全半
    "melodic_minor_up": [0, 2, 3, 5, 7, 9, 11],
    # 旋律小调（下行）：全全全半全半全
    "melodic_minor_down": [0, 2, 4, 5, 7, 8, 10],
    
    # 五声音阶
    # 大调五声音阶
    "pentatonic_major": [0, 2, 4, 7, 9],
    # 小调五声音阶
    "pentatonic_minor": [0, 3, 5, 7, 10],
    # 小调五声音阶（另一种形式）
    "pentatonic_minor_alt": [0, 3, 5, 8, 10],
    # 中国五声音阶（宫商角徵羽）
    "chinese_major": [0, 2, 4, 7, 9],  # 同大调五声
    # 日本音阶
    "japanese": [0, 2, 5, 7, 9],  # 小调五声的一种变体
    
    # 布鲁斯音阶
    # 大调布鲁斯音阶
    "blues_major": [0, 2, 3, 4, 7, 9],
    # 小调布鲁斯音阶
    "blues_minor": [0, 3, 5, 6, 7, 10],
    
    # 教会调式
    # 多利亚调式
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    # 弗里几亚调式
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    # 利底亚调式
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    # 混合利底亚调式
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    # 洛克里亚调式
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    
    # 现代音阶
    # 全音音阶
    "whole_tone": [0, 2, 4, 6, 8, 10],
    # 半音音阶
    "chromatic": list(range(12)),
    # 增三和弦音阶
    "augmented": [0, 3, 4, 7, 8, 11],
    # 减七和弦音阶
    "diminished": [0, 2, 3, 5, 6, 8, 9, 11],
    
    # 其他民族音阶
    # 印度音阶
    "hindustani": [0, 1, 4, 5, 7, 8, 10],  # Bilaval thaat
    # 弗拉明戈音阶
    "flamenco": [0, 1, 3, 4, 5, 7, 8, 10],
    # 吉普赛音阶
    "gypsy": [0, 2, 3, 6, 7, 8, 10],
}


def get_note_from_interval(root_note: NoteName, interval: int) -> NoteName:
    """根据根音和音程计算音符"""
    note_value = (root_note.value + interval) % 12
    return NoteName(note_value)


def get_interval_between_notes(note1: NoteName, note2: NoteName) -> int:
    """计算两个音符之间的音程（半音数）"""
    return (note2.value - note1.value) % 12


def get_interval_name(interval_semitones: int) -> str:
    """根据半音数获取音程名称"""
    if interval_semitones == 0:
        return "纯一度"
    elif interval_semitones == 1:
        return "小二度"
    elif interval_semitones == 2:
        return "大二度"
    elif interval_semitones == 3:
        return "小三度"
    elif interval_semitones == 4:
        return "大三度"
    elif interval_semitones == 5:
        return "纯四度"
    elif interval_semitones == 6:
        return "增四度/减五度"
    elif interval_semitones == 7:
        return "纯五度"
    elif interval_semitones == 8:
        return "小六度"
    elif interval_semitones == 9:
        return "大六度"
    elif interval_semitones == 10:
        return "小七度"
    elif interval_semitones == 11:
        return "大七度"
    elif interval_semitones == 12:
        return "八度"
    else:
        return f"{interval_semitones}度"