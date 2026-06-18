"""
音乐理论核心模块 - 整合音阶、和弦、节奏系统
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
import json

from .notes import NoteName, get_interval_between_notes, get_interval_name
from .scales import Scale, ScaleFactory, ScaleAnalyzer, ScaleType, PREDEFINED_SCALES
from .chords import Chord, ChordFactory, ChordProgressionAnalyzer, ChordUtils, ChordType, PREDEFINED_CHORDS
from .rhythm import RhythmPattern, RhythmFactory, RhythmAnalyzer, TimeSignature, Metronome, COMMON_RHYTHMS
from .chord_progression_generator import (
    ChordProgressionGenerator, 
    ProgressionStyle, 
    ChordProgressionTemplate,
    generate_progression,
    generate_multiple_progressions,
    get_random_progression
)


class MusicTheory:
    """音乐理论核心类"""
    
    def __init__(self):
        self.scales = {}
        self.chords = {}
        self.rhythm_patterns = {}
        self.key_signatures = {}
        self.progression_generator = ChordProgressionGenerator()
        
        # 初始化预定义数据
        self._initialize_data()
    
    def _initialize_data(self):
        """初始化预定义音乐数据"""
        # 加载预定义音阶
        self.scales.update(PREDEFINED_SCALES)
        
        # 加载预定义和弦
        self.chords.update(PREDEFINED_CHORDS)
        
        # 加载预定义节奏模式
        self.rhythm_patterns.update(COMMON_RHYTHMS)
        
        # 建立调性关系
        self._build_key_relationships()
    
    def _build_key_relationships(self):
        """建立调性关系"""
        for root_note in NoteName:
            # 大调和其关系小调
            major_scale = ScaleFactory.create_major_scale(root_note)
            relative_minor = major_scale.get_relative_key()
            
            if relative_minor:
                key = f"{root_note.value_str}_major"
                self.key_signatures[key] = {
                    "scale": major_scale,
                    "relative_minor": relative_minor,
                    "chords": self._get_scale_chords(major_scale)
                }
                
                # 小调版本
                minor_key = f"{relative_minor.root_note.value_str}_minor"
                self.key_signatures[minor_key] = {
                    "scale": relative_minor,
                    "relative_major": major_scale,
                    "chords": self._get_scale_chords(relative_minor)
                }
    
    def _get_scale_chords(self, scale: Scale) -> List[Chord]:
        """获取音阶中的和弦"""
        chords = []
        
        # 为音阶中的每个音创建和弦
        roman_numerals = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
        chord_types = [ChordType.MAJOR, ChordType.MINOR, ChordType.MINOR, 
                      ChordType.MAJOR, ChordType.MAJOR, ChordType.MINOR, ChordType.DIMINISHED]
        
        for i, note in enumerate(scale.notes):
            # 根据音阶位置确定和弦类型
            chord = ChordFactory.create_triad(note, chord_types[i])
            chord.function = roman_numerals[i]
            chords.append(chord)
        
        return chords
    
    # ============ 音阶功能 ============
    
    def create_scale(self, root_note: str, scale_type: str = "major") -> Scale:
        """创建音阶"""
        note = NoteName.from_string(root_note)
        return ScaleFactory.create_scale(note, scale_type)
    
    def get_scale(self, name: str) -> Optional[Scale]:
        """获取预定义音阶"""
        return self.scales.get(name)
    
    def list_scales(self) -> List[str]:
        """列出所有预定义音阶"""
        return list(self.scales.keys())
    
    def analyze_scale(self, scale: Scale) -> Dict[str, Any]:
        """分析音阶"""
        return ScaleAnalyzer.analyze_scale(scale)
    
    def find_scales_with_note(self, note: str) -> List[Scale]:
        """查找包含指定音符的音阶"""
        note_obj = NoteName.from_string(note)
        return ScaleAnalyzer.find_scales_with_note(note_obj)
    
    # ============ 和弦功能 ============
    
    def create_chord(self, root_note: str, chord_type: str = "major") -> Chord:
        """创建和弦"""
        note = NoteName.from_string(root_note)
        return ChordFactory.create_chord(note, chord_type)
    
    def get_chord(self, name: str) -> Optional[Chord]:
        """获取预定义和弦"""
        return self.chords.get(name)
    
    def list_chords(self) -> List[str]:
        """列出所有预定义和弦"""
        return list(self.chords.keys())
    
    def get_chord_formula(self, chord_type: str) -> str:
        """获取和弦公式"""
        return ChordUtils.get_chord_formula(chord_type)
    
    def get_chord_inversions(self, chord: Chord) -> List[Chord]:
        """获取和弦转位"""
        return chord.get_inversions()
    
    # ============ 节奏功能 ============
    
    def create_rhythm_pattern(self, pattern_type: str, **kwargs) -> RhythmPattern:
        """创建节奏模式"""
        factory_map = {
            "rock": RhythmFactory.create_rock_beat,
            "waltz": RhythmFactory.create_waltz,
            "funk": RhythmFactory.create_funk,
            "swing": RhythmFactory.create_swing,
            "blues": RhythmFactory.create_blues,
        }
        
        factory = factory_map.get(pattern_type)
        if factory:
            return factory(**kwargs)
        else:
            raise ValueError(f"未知的节奏类型: {pattern_type}")
    
    def get_rhythm_pattern(self, name: str) -> Optional[RhythmPattern]:
        """获取预定义节奏模式"""
        return self.rhythm_patterns.get(name)
    
    def list_rhythm_patterns(self) -> List[str]:
        """列出所有预定义节奏模式"""
        return list(self.rhythm_patterns.keys())
    
    def analyze_rhythm(self, pattern: RhythmPattern) -> Dict[str, Any]:
        """分析节奏模式"""
        return RhythmAnalyzer.analyze_pattern(pattern)
    
    # ============ 和弦进行功能 ============
    
    def create_progression(self, chord_names: List[str]) -> List[Chord]:
        """创建和弦进行"""
        progression = []
        for chord_name in chord_names:
            chord = self.get_chord(chord_name)
            if chord:
                progression.append(chord)
        return progression
    
    def analyze_progression(self, progression: List[Chord]) -> Dict[str, Any]:
        """分析和弦进行"""
        return ChordProgressionAnalyzer.analyze_progression(progression)
    
    def get_related_chords(self, chord: Chord, scale: Scale) -> List[Chord]:
        """获取音阶中的相关和弦"""
        return ChordProgressionAnalyzer.find_related_chords(chord, scale)
    
    # ============ 和弦进行生成功能 ============
    
    def generate_chord_progression(self, root_note: str, scale_type: str = "major", 
                                 style: ProgressionStyle = ProgressionStyle.CLASSIC_POP, 
                                 length: int = 4, variation: float = 0.1) -> List[Chord]:
        """生成和弦进行"""
        return self.progression_generator.generate_progression(
            root_note, scale_type, style, length, variation
        )
    
    def generate_multiple_chord_progressions(self, root_note: str, scale_type: str = "major",
                                          styles: Optional[List[ProgressionStyle]] = None,
                                          count: int = 5, length: int = 4) -> Dict[ProgressionStyle, List[Chord]]:
        """生成多种风格的和弦进行"""
        return self.progression_generator.generate_multiple_progressions(
            root_note, scale_type, styles, count, length
        )
    
    def get_random_chord_progression(self, root_note: str, scale_type: str = "major", length: int = 4) -> List[Chord]:
        """生成随机和弦进行"""
        return self.progression_generator.get_random_progression(root_note, scale_type, length)
    
    def analyze_progression_tension(self, progression: List[Chord]) -> Dict[str, Any]:
        """分析和弦进行紧张度"""
        return self.progression_generator.analyze_progression_tension(progression)
    
    def get_progression_improvements(self, progression: List[Chord]) -> List[str]:
        """获取和弦进行改进建议"""
        return self.progression_generator.suggest_improvements(progression)
    
    def list_progression_styles(self) -> List[str]:
        """列出可用的和弦进行风格"""
        return [style.value for style in ProgressionStyle.get_styles()]
    
    def get_progression_style_info(self, style: ProgressionStyle) -> Dict[str, Any]:
        """获取和弦进行风格信息"""
        template = self.progression_generator.get_template_by_style(style)
        info = {
            "name": template.name,
            "style": style.value,
            "description": ProgressionStyle.get_description(style),
            "complexity": template.complexity,
            "popularity": template.popularity,
            "example_functions": template.chord_functions,
            "example_chord_types": template.chord_types
        }
        return info
    
    # ============ 调性关系功能 ============
    
    def get_key_relationships(self, key: str) -> Dict[str, Any]:
        """获取调性关系"""
        return self.key_signatures.get(key, {})
    
    def get_relative_keys(self, key: str) -> List[str]:
        """获取关系调性"""
        relationships = self.get_key_relationships(key)
        relative_keys = []
        
        if "relative_minor" in relationships:
            relative_keys.append(f"{relationships['relative_minor'].root_note.value_str}_minor")
        
        if "relative_major" in relationships:
            relative_keys.append(f"{relationships['relative_major'].root_note.value_str}_major")
        
        return relative_keys
    
    # ============ 音乐分析功能 ============
    
    def analyze_music_element(self, element: Union[Scale, Chord, RhythmPattern]) -> Dict[str, Any]:
        """分析音乐元素"""
        if isinstance(element, Scale):
            return self.analyze_scale(element)
        elif isinstance(element, Chord):
            return {
                "name": element.name,
                "type": element.chord_type,
                "notes": [note.value_str for note in element.notes],
                "function": element.function
            }
        elif isinstance(element, RhythmPattern):
            return self.analyze_rhythm(element)
        else:
            return {"error": "不支持的音乐元素类型"}
    
    def get_harmony_suggestions(self, scale: Scale, progression_length: int = 4) -> List[List[Chord]]:
        """获取和声建议"""
        suggestions = []
        
        # 基本的和弦进行
        basic_progressions = [
            ["I", "IV", "V", "I"],
            ["vi", "IV", "I", "V"],
            ["ii", "V", "I"],
            ["I", "V", "vi", "IV"],
        ]
        
        for prog in basic_progressions:
            chord_progression = []
            for func in prog:
                # 在音阶中找到对应功能的和弦
                for chord in self._get_scale_chords(scale):
                    if chord.function == func:
                        chord_progression.append(chord)
                        break
            
            if len(chord_progression) == len(prog):
                suggestions.append(chord_progression)
        
        return suggestions[:progression_length]  # 返回前4个建议
    
    # ============ 工具功能 ============
    
    def validate_music_data(self, data: Dict[str, Any]) -> List[str]:
        """验证音乐数据"""
        errors = []
        
        if "scales" in data:
            for scale_data in data["scales"]:
                if not scale_data.get("name"):
                    errors.append("音阶名称不能为空")
        
        if "chords" in data:
            for chord_data in data["chords"]:
                if not chord_data.get("name"):
                    errors.append("和弦名称不能为空")
        
        return errors
    
    def export_data(self, filename: str = "music_data.json"):
        """导出音乐数据"""
        data = {
            "scales": {name: scale.to_dict() for name, scale in self.scales.items()},
            "chords": {name: chord.to_dict() for name, chord in self.chords.items()},
            "rhythm_patterns": {name: pattern.to_dict() for name, pattern in self.rhythm_patterns.items()},
            "key_signatures": {key: {
                "scale": scale.to_dict(),
                "relative_minor": rel_minor.to_dict() if rel_minor else None,
                "chords": [chord.to_dict() for chord in chords]
            } for key, (scale, rel_minor, chords) in self.key_signatures.items()}
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return data
    
    def import_data(self, filename: str):
        """从文件导入音乐数据"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证数据
            errors = self.validate_music_data(data)
            if errors:
                raise ValueError(f"数据验证失败: {', '.join(errors)}")
            
            # 这里可以添加具体的数据导入逻辑
            # 例如重建Scale、Chord、RhythmPattern对象
            
            return True
        except Exception as e:
            print(f"导入数据失败: {e}")
            return False
    
    # ============ 示例和演示功能 ============
    
    def get_examples(self) -> Dict[str, Any]:
        """获取音乐理论的示例"""
        examples = {
            "scales": {
                "C_major": self.create_scale("C", "major"),
                "A_minor": self.create_scale("A", "natural_minor"),
                "C_pentatonic": self.create_scale("C", "pentatonic_major"),
            },
            "chords": {
                "C_major": self.create_chord("C", "major"),
                "A_minor": self.create_chord("A", "minor"),
                "G_seventh": self.create_chord("G", "dominant7"),
            },
            "rhythm_patterns": {
                "rock": self.create_rhythm_pattern("rock"),
                "waltz": self.create_rhythm_pattern("waltz"),
            },
            "progressions": {
                "basic": self.create_progression(["C_major", "G_major", "A_minor", "F_major"])
            }
        }
        
        return examples
    
    def demonstrate_theory_concepts(self):
        """演示音乐理论概念"""
        print("=== 音乐理论概念演示 ===")
        
        # 1. 音阶演示
        print("\n1. 音阶演示:")
        c_major = self.create_scale("C", "major")
        print(f"C大调音阶: {[note.value_str for note in c_major.notes]}")
        print(f"关系小调: {c_major.get_relative_key().name if c_major.get_relative_key() else '无'}")
        
        # 2. 和弦演示
        print("\n2. 和弦演示:")
        c_chord = self.create_chord("C", "major")
        print(f"C大和弦构成: {[note.value_str for note in c_chord.notes]}")
        inversions = c_chord.get_inversions()
        print(f"第一转位: {inversions[0].name if inversions else '无转位'}")
        
        # 3. 节奏演示
        print("\n3. 节奏演示:")
        rock_pattern = self.create_rhythm_pattern("rock")
        print(f"摇滚节奏: {rock_pattern.name} ({rock_pattern.bpm} BPM)")
        print(f"每小节拍数: {rock_pattern.time_signature.beats_per_measure}")
        
        # 4. 和弦进行演示
        print("\n4. 和弦进行演示:")
        progression = self.create_progression(["C_major", "G_major", "A_minor", "F_major"])
        analysis = self.analyze_progression(progression)
        print(f"和弦进行长度: {analysis['length']}")
        print(f"根音运动: {analysis['root_movement']}")


# ============ 全局实例 ============
music_theory = MusicTheory()


# ============ 快捷函数 ============

def create_scale(root_note: str, scale_type: str = "major") -> Scale:
    """快捷函数：创建音阶"""
    return music_theory.create_scale(root_note, scale_type)

def create_chord(root_note: str, chord_type: str = "major") -> Chord:
    """快捷函数：创建和弦"""
    return music_theory.create_chord(root_note, chord_type)

def create_rhythm(pattern_type: str, **kwargs) -> RhythmPattern:
    """快捷函数：创建节奏模式"""
    return music_theory.create_rhythm_pattern(pattern_type, **kwargs)

def analyze_progression(chord_names: List[str]) -> Dict[str, Any]:
    """快捷函数：分析和弦进行"""
    progression = music_theory.create_progression(chord_names)
    return music_theory.analyze_progression(progression)

def generate_chord_progression(root_note: str, scale_type: str = "major", 
                             style: ProgressionStyle = ProgressionStyle.CLASSIC_POP, 
                             length: int = 4, variation: float = 0.1) -> List[Chord]:
    """快捷函数：生成和弦进行"""
    return music_theory.generate_chord_progression(root_note, scale_type, style, length, variation)

def get_random_chord_progression(root_note: str, scale_type: str = "major", length: int = 4) -> List[Chord]:
    """快捷函数：生成随机和弦进行"""
    return music_theory.get_random_chord_progression(root_note, scale_type, length)


if __name__ == "__main__":
    # 运行演示
    music_theory.demonstrate_theory_concepts()