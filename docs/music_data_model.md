# 🎵 Evo Music 数据模型设计

## 1. 音阶系统 (Scale)

### 1.1 音阶类型定义
```python
class ScaleType:
    MAJOR = "major"           # 大调
    MINOR = "minor"           # 小调
    NATURAL_MINOR = "natural_minor"  # 自然小调
    HARMONIC_MINOR = "harmonic_minor"  # 和声小调
    MELODIC_MINOR = "melodic_minor"    # 旋律小调
    PENTATONIC_MAJOR = "pentatonic_major"  # 大调五声音阶
    PENTATONIC_MINOR = "pentatonic_minor"  # 小调五声音阶
    BLUES_MAJOR = "blues_major"         # 大调布鲁斯
    BLUES_MINOR = "blues_minor"         # 小调布鲁斯
    DORIAN = "dorian"         # 多利亚调式
    PHRYGIAN = "phrygian"     # 弗里几亚调式
    LYDIAN = "lydian"         # 利底亚调式
    MIXOLYDIAN = "mixolydian" # 混合利底亚调式
    LOCRIAN = "locrian"       # 洛克里亚调式
```

### 1.2 音阶数据结构
```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class NoteName(Enum):
    C = "C"
    C_SHARP = "C#"
    D = "D"
    D_SHARP = "D#"
    E = "E"
    F = "F"
    F_SHARP = "F#"
    G = "G"
    G_SHARP = "G#"
    A = "A"
    A_SHARP = "A#"
    B = "B"

@dataclass
class Scale:
    """音阶数据结构"""
    name: str                    # 音阶名称（如："C Major"）
    scale_type: str              # 音阶类型（ScaleType枚举值）
    root_note: NoteName          # 根音
    intervals: List[int]         # 音程模式（相对于根音的半音数）
    notes: List[NoteName]        # 构成音
    description: str             # 音阶描述
    
    def get_note_at_position(self, position: int) -> Optional[NoteName]:
        """获取音阶中指定位置的音"""
        if 0 <= position < len(self.notes):
            return self.notes[position]
        return None
    
    def get_chords_for_scale(self) -> List[str]:
        """获取该音阶常用的和弦"""
        # 根据音阶类型返回推荐和弦
        pass

# 音阶模式定义（相对于根音的半音数）
SCALE_INTERVALS = {
    ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],           # 全全半全全半全
    ScaleType.MINOR: [0, 2, 3, 5, 7, 8, 10],          # 全半全全半全全
    ScaleType.PENTATONIC_MAJOR: [0, 2, 4, 7, 9],       # 大调五声
    ScaleType.PENTATONIC_MINOR: [0, 3, 5, 7, 10],     # 小调五声
    ScaleType.BLUES_MAJOR: [0, 2, 3, 4, 7, 9],        # 大调布鲁斯
    ScaleType.BLUES_MINOR: [0, 3, 5, 6, 7, 10],       # 小调布鲁斯
}

# 预定义常用音阶
MAJOR_SCALES = {}
MINOR_SCALES = {}
PENTATONIC_SCALES = {}
BLUES_SCALES = {}
```

### 1.3 音阶工厂类
```python
class ScaleFactory:
    """音阶工厂类，用于创建各种音阶"""
    
    @staticmethod
    def create_major_scale(root_note: NoteName) -> Scale:
        """创建大调音阶"""
        intervals = SCALE_INTERVALS[ScaleType.MAJOR]
        notes = []
        current_note = root_note.value
        
        # 根据音程模式计算音符
        for interval in intervals:
            # 这里需要实现音符到音符索引的计算逻辑
            notes.append(NoteName((NoteName(root_note.value).value + interval) % 12))
        
        return Scale(
            name=f"{root_note.value} Major",
            scale_type=ScaleType.MAJOR,
            root_note=root_note,
            intervals=intervals,
            notes=notes,
            description="大调音阶，明亮的色彩"
        )
    
    @staticmethod
    def create_minor_scale(root_note: NoteName, minor_type: str = "natural") -> Scale:
        """创建小调音阶"""
        if minor_type == "natural":
            intervals = SCALE_INTERVALS[ScaleType.MINOR]
        elif minor_type == "harmonic":
            intervals = [0, 2, 3, 5, 7, 8, 11]  # 和声小调：第7级升高半音
        elif minor_type == "melodic":
            intervals = [0, 2, 3, 5, 7, 9, 11]  # 旋律小调：上下行不同
        
        # 计算音符...
        
        return Scale(
            name=f"{root_note.value} {minor_type.capitalize()} Minor",
            scale_type=f"{minor_type}_minor",
            root_note=root_note,
            intervals=intervals,
            notes=[],  # 需要计算
            description=f"小调音阶（{minor_type}）"
        )
```

## 2. 和弦系统 (Chord)

### 2.1 和弦类型定义
```python
class ChordType(Enum):
    MAJOR = "major"           # 大三和弦
    MINOR = "minor"           # 小三和弦
    AUGMENTED = "augmented"   # 增三和弦
    DIMINISHED = "diminished" # 减三和弦
    MAJOR7 = "major7"         # 大七和弦
    MINOR7 = "minor7"         # 小七和弦
    DOMINANT7 = "dominant7"   # 属七和弦
    AUGMENTED7 = "augmented7" # 增七和弦
    DIMINISHED7 = "diminished7" # 减七和弦
    HALF_DIMINISHED7 = "half_diminished7" # 半减七和弦
    MAJOR9 = "major9"         # 大九和弦
    MINOR9 = "minor9"         # 小九和弦
    DOMINANT9 = "dominant9"   # 属九和弦
    MAJOR11 = "major11"       # 大十一和弦
    MINOR11 = "minor11"       # 小十一和弦
    DOMINANT11 = "dominant11" # 属十一和弦
    MAJOR13 = "major13"       # 大十三和弦
    MINOR13 = "minor13"       # 小十三和弦
    DOMINANT13 = "dominant13" # 属十三和弦
```

### 2.2 和弦数据结构
```python
@dataclass
class Chord:
    """和弦数据结构"""
    name: str                    # 和弦名称（如："C Major"）
    chord_type: str              # 和弦类型（ChordType枚举值）
    root_note: NoteName          # 根音
    bass_note: Optional[NoteName] # 低音（用于转位）
    notes: List[NoteName]        # 构成音
    extensions: List[int]        # 扩展音（9th, 11th, 13th）
    description: str             # 和弦描述
    function: Optional[str]      # 功能（如：I, ii, iii, IV, V, vi, vii°）
    
    def get_note_at_position(self, position: int) -> Optional[NoteName]:
        """获取和弦中指定位置的音"""
        if 0 <= position < len(self.notes):
            return self.notes[position]
        return None
    
    def is_seventh_chord(self) -> bool:
        """是否为七和弦"""
        return 7 in [note.value % 12 for note in self.notes]
    
    def is_ninth_chord(self) -> bool:
        """是否为九和弦"""
        return 9 in [note.value % 12 for note in self.notes]

# 和弦模式定义（相对于根音的半音数）
CHORD_INTERVALS = {
    ChordType.MAJOR: [0, 4, 7],                     # 大三和弦
    ChordType.MINOR: [0, 3, 7],                     # 小三和弦
    ChordType.AUGMENTED: [0, 4, 8],                 # 增三和弦
    ChordType.DIMINISHED: [0, 3, 6],                # 减三和弦
    ChordType.MAJOR7: [0, 4, 7, 11],               # 大七和弦
    ChordType.MINOR7: [0, 3, 7, 10],               # 小七和弦
    ChordType.DOMINANT7: [0, 4, 7, 10],            # 属七和弦
    ChordType.AUGMENTED7: [0, 4, 8, 10],           # 增七和弦
    ChordType.DIMINISHED7: [0, 3, 6, 9],           # 减七和弦
    ChordType.HALF_DIMINISHED7: [0, 3, 6, 10],     # 半减七和弦
}
```

### 2.3 和弦工厂类
```python
class ChordFactory:
    """和弦工厂类"""
    
    @staticmethod
    def create_triad(root_note: NoteName, chord_type: ChordType) -> Chord:
        """创建三和弦"""
        intervals = CHORD_INTERVALS.get(chord_type, [0, 4, 7])
        notes = []
        
        for interval in intervals:
            notes.append(NoteName((NoteName(root_note.value).value + interval) % 12))
        
        return Chord(
            name=f"{root_note.value} {chord_type.value}",
            chord_type=chord_type.value,
            root_note=root_note,
            bass_note=None,
            notes=notes,
            extensions=[],
            description=f"{chord_type.value} 三和弦",
            function=None
        )
    
    @staticmethod
    def create_seventh_chord(root_note: NoteName, chord_type: ChordType) -> Chord:
        """创建七和弦"""
        intervals = CHORD_INTERVALS.get(chord_type, [0, 4, 7, 10])
        notes = []
        
        for interval in intervals:
            notes.append(NoteName((NoteName(root_note.value).value + interval) % 12))
        
        return Chord(
            name=f"{root_note.value} {chord_type.value}",
            chord_type=chord_type.value,
            root_note=root_note,
            bass_note=None,
            notes=notes,
            extensions=[7],
            description=f"{chord_type.value} 七和弦",
            function=None
        )
```

## 3. 节奏系统 (Rhythm)

### 3.1 节奏基础数据结构
```python
class TimeSignature(Enum):
    """拍号"""
    FOUR_FOUR = "4/4"          # 4/4拍
    THREE_FOUR = "3/4"         # 3/4拍
    TWO_FOUR = "2/4"          # 2/4拍
    SIX_EIGHT = "6/8"         # 6/8拍
    TWELVE_EIGHT = "12/8"     # 12/8拍

class NoteDuration(Enum):
    """音符时值"""
    WHOLE = 1.0               # 全音符
    HALF = 0.5               # 二分音符
    QUARTER = 0.25           # 四分音符
    EIGHTH = 0.125           # 八分音符
    SIXTEENTH = 0.0625       # 十六分音符
    THIRTY_SECOND = 0.03125  # 三十二分音符

class NoteValue(Enum):
    """音符值"""
    WHOLE = "𝅝"
    HALF = "𝅗𝅥"
    QUARTER = "♩"
    EIGHTH = "♪"
    SIXTEENTH = "♬"
    REST = "𝄽"

@dataclass
class NoteEvent:
    """音符事件"""
    note_name: Optional[NoteName]    # 音名（None为休止符）
    duration: float                  # 时值（拍数）
    velocity: int                    # 力度（0-127）
    tie: bool = False               # 是否延音
    dotted: bool = False            # 是否附点
    
    def get_total_duration(self) -> float:
        """获取总时长（考虑附点）"""
        if self.dotted:
            return self.duration * 1.5
        return self.duration
```

### 3.2 节奏模式数据结构
```python
@dataclass
class RhythmPattern:
    """节奏模式"""
    name: str                        # 模式名称（如："Rock Beat"）
    time_signature: TimeSignature    # 拍号
    beats_per_measure: int           # 每小节拍数
    note_events: List[NoteEvent]     # 音符事件列表
    bpm: int = 120                   # 速度
    description: str = ""            # 描述
    
    def get_duration(self) -> float:
        """获取模式总时长"""
        return sum(event.get_total_duration() for event in self.note_events)
    
    def repeat(self, times: int) -> List[NoteEvent]:
        """重复节奏模式"""
        repeated = []
        for _ in range(times):
            repeated.extend(self.note_events)
        return repeated

# 常用节奏模式库
COMMON_RHYTHMS = {
    "rock_beat": RhythmPattern(
        name="Rock Beat",
        time_signature=TimeSignature.FOUR_FOUR,
        beats_per_measure=4,
        note_events=[
            NoteEvent(None, NoteDuration.QUARTER.value, 80),
            NoteEvent(None, NoteDuration.EIGHTH.value, 100),
            NoteEvent(None, NoteDuration.EIGHTH.value, 100),
        ],
        bpm=120,
        description="经典摇滚节奏"
    ),
    
    "waltz": RhythmPattern(
        name="Waltz",
        time_signature=TimeSignature.THREE_FOUR,
        beats_per_measure=3,
        note_events=[
            NoteEvent(None, NoteDuration.QUARTER.value, 80),
            NoteEvent(None, NoteDuration.QUARTER.value, 80),
            NoteEvent(None, NoteDuration.QUARTER.value, 80),
        ],
        bpm=100,
        description="华尔兹节奏"
    ),
}
```

### 3.3 节拍器类
```python
class Metronome:
    """节拍器类"""
    
    def __init__(self, bpm: int = 120, time_signature: TimeSignature = TimeSignature.FOUR_FOUR):
        self.bpm = bpm
        self.time_signature = time_signature
        self.current_beat = 0
        
    def get_beat_interval(self) -> float:
        """获取节拍间隔（秒）"""
        return 60.0 / self.bpm
    
    def next_beat(self):
        """下一拍"""
        beats_per_measure = self.time_signature.value.split('/')[0]
        self.current_beat = (self.current_beat + 1) % int(beats_per_measure)
        return self.current_beat + 1  # 返回1开始的节拍号
```

## 4. 音乐理论工具类

### 4.1 调性关系
```python
class KeyRelationships:
    """调性关系"""
    
    @staticmethod
    def get_relative_major(key_note: NoteName) -> NoteName:
        """获取关系大调"""
        # 小调的关系大调是上方小三度
        major_notes = [NoteName.C, NoteName.D, NoteName.E, NoteName.F, 
                      NoteName.G, NoteName.A, NoteName.B]
        minor_notes = [NoteName.A, NoteName.B, NoteName.C, NoteName.D,
                      NoteName.E, NoteName.F, NoteName.G]
        
        try:
            index = minor_notes.index(key_note)
            return major_notes[index]
        except ValueError:
            return key_note
    
    @staticmethod
    def get_parallel_minor(key_note: NoteName) -> NoteName:
        """获取平行小调"""
        return key_note  # 同主音小调
    
    @staticmethod
    def get_circle_of_fifths(current_note: NoteName, direction: str = "clockwise", steps: int = 1) -> NoteName:
        """获取五度圈上的下一个音"""
        circle_clockwise = [NoteName.C, NoteName.G, NoteName.D, NoteName.A, 
                          NoteName.E, NoteName.B, NoteName.F_SHARP, 
                          NoteName.C_SHARP, NoteName.G_SHARP, NoteName.D_SHARP, 
                          NoteName.A_SHARP, NoteName.F]
        
        circle_counterclockwise = circle_clockwise[::-1]
        
        if direction == "clockwise":
            circle = circle_clockwise
        else:
            circle = circle_counterclockwise
        
        try:
            index = circle.index(current_note)
            return circle[(index + steps) % len(circle)]
        except ValueError:
            return current_note
```

### 4.2 和弦进行分析
```python
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
        }
        
        # 识别常见和弦进行
        common_patterns = [
            ["I", "IV", "V", "I"],      # 1-4-5-1
            ["vi", "IV", "I", "V"],      # 6-4-1-5
            ["ii", "V", "I"],            # 2-5-1
        ]
        
        return analysis
```

## 5. 数据验证和转换

### 5.1 验证器
```python
class MusicDataValidator:
    """音乐数据验证器"""
    
    @staticmethod
    def validate_scale(scale: Scale) -> List[str]:
        """验证音阶数据"""
        errors = []
        
        if not scale.name:
            errors.append("音阶名称不能为空")
        
        if not scale.root_note:
            errors.append("音阶根音不能为空")
        
        if len(scale.intervals) == 0:
            errors.append("音程模式不能为空")
            
        return errors
    
    @staticmethod
    def validate_chord(chord: Chord) -> List[str]:
        """验证和弦数据"""
        errors = []
        
        if not chord.name:
            errors.append("和弦名称不能为空")
            
        if not chord.root_note:
            errors.append("和弦根音不能为空")
            
        return errors
```

## 6. 导出和序列化

### 6.1 JSON序列化支持
```python
import json

class MusicDataEncoder(json.JSONEncoder):
    """音乐数据JSON编码器"""
    
    def default(self, obj):
        if isinstance(obj, Scale):
            return {
                'name': obj.name,
                'scale_type': obj.scale_type,
                'root_note': obj.root_note.value,
                'intervals': obj.intervals,
                'notes': [note.value for note in obj.notes],
                'description': obj.description
            }
        elif isinstance(obj, Chord):
            return {
                'name': obj.name,
                'chord_type': obj.chord_type,
                'root_note': obj.root_note.value,
                'bass_note': obj.bass_note.value if obj.bass_note else None,
                'notes': [note.value for note in obj.notes],
                'extensions': obj.extensions,
                'description': obj.description,
                'function': obj.function
            }
        elif isinstance(obj, NoteName):
            return obj.value
        else:
            return super().default(obj)

def save_music_data(data: dict, filename: str):
    """保存音乐数据到JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, cls=MusicDataEncoder, indent=2, ensure_ascii=False)

def load_music_data(filename: str) -> dict:
    """从JSON文件加载音乐数据"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
```

## 7. 测试和示例

### 7.1 单元测试
```python
# 测试音阶创建
def test_scale_creation():
    c_major = ScaleFactory.create_major_scale(NoteName.C)
    assert c_major.name == "C Major"
    assert c_major.scale_type == ScaleType.MAJOR
    assert len(c_major.notes) == 7

# 测试和弦创建
def test_chord_creation():
    c_major = ChordFactory.create_triad(NoteName.C, ChordType.MAJOR)
    assert c_major.name == "C major"
    assert len(c_major.notes) == 3

# 测试节奏模式
def test_rhythm_pattern():
    rock_pattern = COMMON_RHYTHMS["rock_beat"]
    assert rock_pattern.name == "Rock Beat"
    assert rock_pattern.time_signature == TimeSignature.FOUR_FOUR
```

### 7.2 使用示例
```python
# 创建音阶
c_major = ScaleFactory.create_major_scale(NoteName.C)
a_minor = ScaleFactory.create_minor_scale(NoteName.A, "natural")

# 创建和弦
c_major_chord = ChordFactory.create_triad(NoteName.C, ChordType.MAJOR)
g_major_chord = ChordFactory.create_triad(NoteName.G, ChordType.MAJOR)
f_major_chord = ChordFactory.create_triad(NoteName.F, ChordType.MAJOR)

# 创建节奏模式
rock_beat = COMMON_RHYTHMS["rock_beat"]
waltz_pattern = COMMON_RHYTHMS["waltz"]

# 生成和弦进行
progression = [c_major_chord, g_major_chord, c_major_chord, f_major_chord]

# 分析和弦进行
analysis = ChordProgressionAnalyzer.analyze_progression(progression)

# 保存数据
music_data = {
    "scales": [c_major, a_minor],
    "chords": [c_major_chord, g_major_chord, f_major_chord],
    "rhythm_patterns": [rock_beat, waltz_pattern]
}
save_music_data(music_data, "music_data.json")
```

这个数据模型设计涵盖了音乐理论的核心元素，提供了完整的音阶、和弦和节奏系统。设计具有以下特点：

1. **完整性和扩展性**：涵盖了主要的音阶类型、和弦类型和节奏模式
2. **类型安全**：使用枚举和数据类确保数据类型正确
3. **模块化设计**：工厂类和工具类分离，便于维护和扩展
4. **实际应用支持**：包含JSON序列化、验证器等实用功能
5. **测试友好**：提供完整的单元测试和使用示例

该设计可以作为Evo Music项目的基础数据模型，支持后续的旋律生成、和弦进行优化等高级功能。