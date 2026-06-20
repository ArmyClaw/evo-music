"""
音乐曲式结构模块 - 实现各种音乐曲式结构，包括 A-B-A 曲式
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import random

from .notes import NoteName
from .scales import Scale, ScaleType, ScaleFactory
from .melody import MelodyConfig, EmotionType, MarkovMelodyGenerator
from .harmony_arranger import HarmonyArranger, HarmonyConfig, HarmonyStyle
from .music_theory import MusicTheory


class FormType(Enum):
    """曲式类型"""
    ABA = "aba"                  # A-B-A 曲式
    RONDO = "rondo"             # 回旋曲式
    SONATA = "sonata"           # 奏鸣曲式
    THEME_VARIATIONS = "theme_variations"  # 主题与变奏
    MINUET = "minuet"          # 小步舞曲
    SCHERZO = "scherzo"         # 谐谑曲
    FUGUE = "fugue"            # 赋格


class SectionRole(Enum):
    """段落角色"""
    THEME_A = "theme_a"         # A段（主题）
    CONTRAST_B = "contrast_b"   # B段（对比）
    THEME_RETURN_A = "theme_return_a"  # A段再现
    DEVELOPMENT = "development"  # 展开部
    CODA = "coda"              # 尾声
    BRIDGE = "bridge"          # 过渡段
    INTRODUCTION = "introduction"  # 引子


@dataclass
class SectionConfig:
    """段落配置"""
    role: SectionRole
    length: int                 # 段落长度（小节数）
    emotion: EmotionType        # 段落情感
    tempo_change: float = 1.0    # 速度变化倍数
    dynamic_level: float = 1.0   # 力度等级
    transposition: int = 0      # 移调（半音）
    
    def __post_init__(self):
        # 根据情感自动设置参数
        if self.emotion == EmotionType.HAPPY:
            self.dynamic_level = 1.2
        elif self.emotion == EmotionType.SAD:
            self.dynamic_level = 0.7
        elif self.emotion == EmotionType.EPIC:
            self.dynamic_level = 1.5
        elif self.emotion == EmotionType.PEACEFUL:
            self.dynamic_level = 0.8


@dataclass
class ABAConfig:
    """A-B-A 曲式配置"""
    a_section: SectionConfig    # A段配置
    b_section: SectionConfig    # B段配置
    return_section: SectionConfig # A段再现配置
    
    # 全局参数
    key: str = "C"             # 主调
    scale_type: ScaleType = ScaleType.MAJOR
    tempo: int = 120
    time_signature: Tuple[int, int] = (4, 4)
    
    # 细节参数
    transition_length: int = 2   # 过渡长度
    coda_length: int = 4       # 尾声长度
    repeat_a_section: bool = True  # 是否重复A段
    
    @classmethod
    def create_classical_aba(cls):
        """创建古典A-B-A曲式配置"""
        return cls(
            a_section=SectionConfig(
                role=SectionRole.THEME_A,
                length=8,
                emotion=EmotionType.HAPPY,
                dynamic_level=1.0
            ),
            b_section=SectionConfig(
                role=SectionRole.CONTRAST_B,
                length=8,
                emotion=EmotionType.SAD,
                dynamic_level=0.8,
                transposition=5  # 五度关系，形成对比
            ),
            return_section=SectionConfig(
                role=SectionRole.THEME_RETURN_A,
                length=8,
                emotion=EmotionType.HAPPY,
                dynamic_level=1.2  # 再现时加强力度
            ),
            key="C",
            scale_type=ScaleType.MAJOR,
            tempo=120,
            time_signature=(4, 4),
            repeat_a_section=True
        )
    
    @classmethod
    def create_modern_aba(cls):
        """创建现代A-B-A曲式配置"""
        return cls(
            a_section=SectionConfig(
                role=SectionRole.THEME_A,
                length=16,
                emotion=EmotionType.NEUTRAL,
                dynamic_level=1.0
            ),
            b_section=SectionConfig(
                role=SectionRole.CONTRAST_B,
                length=16,
                emotion=EmotionType.MYSTERIOUS,
                dynamic_level=0.9,
                tempo_change=0.8  # 稍微放慢速度
            ),
            return_section=SectionConfig(
                role=SectionRole.THEME_RETURN_A,
                length=16,
                emotion=EmotionType.BRIGHT,
                dynamic_level=1.3  # 再现时更加明亮
            ),
            key="C",
            scale_type=ScaleType.MAJOR,
            tempo=100,
            time_signature=(4, 4),
            repeat_a_section=False
        )


class ABAFormGenerator:
    """A-B-A 曲式生成器"""
    
    def __init__(self, config: ABAConfig):
        self.config = config
        self.scale_factory = ScaleFactory()
        self.music_theory = MusicTheory()
        
        # 创建调式
        root_note = NoteName.from_string(config.key)
        self.scale = self.scale_factory.create_scale(
            root_note,
            config.scale_type  # ScaleType 枚举值
        )
        
        # 创建默认的旋律配置
        default_melody_config = MelodyConfig(
            scale=self.scale,
            emotion=config.a_section.emotion
        )
        self.melody_generator = MarkovMelodyGenerator(default_melody_config)
    
    def generate_aba_structure(self) -> Dict[str, Any]:
        """生成A-B-A曲式结构"""
        print("🎼 生成 A-B-A 曲式结构...")
        
        # 生成各段落
        sections = {}
        
        # A段（主题）
        print("  📜 生成 A 段（主题）...")
        sections['a_section'] = self._generate_section(
            self.config.a_section, is_theme=True
        )
        
        # B段（对比部）
        print("  🔄 生成 B 段（对比部）...")
        sections['b_section'] = self._generate_section(
            self.config.b_section, is_contrast=True
        )
        
        # A段再现
        print("  🎭 再现 A 段...")
        sections['return_section'] = self._generate_section(
            self.config.return_section, is_return=True
        )
        
        # 生成过渡段
        if self.config.transition_length > 0:
            print("  🌉 生成过渡段...")
            sections['transitions'] = self._generate_transitions()
        
        # 生成尾声
        if self.config.coda_length > 0:
            print("  🎉 生成尾声...")
            sections['coda'] = self._generate_coda()
        
        # 组织完整曲式
        aba_structure = {
            "form_type": "A-B-A",
            "config": self.config,
            "sections": sections,
            "total_measures": self._calculate_total_measures(sections),
            "midi_data": self._generate_complete_midi(sections)
        }
        
        return aba_structure
    
    def _generate_section(self, section_config: SectionConfig, 
                         is_theme: bool = False, 
                         is_contrast: bool = False,
                         is_return: bool = False) -> Dict[str, Any]:
        """生成单个段落"""
        # 创建段落特定的配置
        melody_config = MelodyConfig(
            scale=self.scale,
            emotion=section_config.emotion,
            length=section_config.length * 4,  # 转换为拍数
            tempo=int(self.config.tempo * section_config.tempo_change),
            start_octave=4 if is_theme else (3 if is_contrast else 4),
            enable_optimization=True,
            use_harmony_optimization=True
        )
        
        # 生成旋律
        melody_states = self.melody_generator.generate()
        # 转换为音符列表
        melody_notes = [(state.note.value, state.duration) for state in melody_states]
        
        # 生成和声
        harmony_config = HarmonyConfig.get_default_for_emotion(section_config.emotion)
        harmony_config.style = HarmonyStyle.POP if is_theme else (
            HarmonyStyle.JAZZ if is_contrast else HarmonyStyle.POP
        )
        
        harmony_arranger = HarmonyArranger(harmony_config)
        harmony = harmony_arranger.arrange_harmony_for_melody(
            melody_notes, self.scale, self.config.time_signature
        )
        
        # 应用段落特定调整
        adjusted_melody = melody_notes  # 简化实现，直接返回原始旋律
        
        return {
            "config": section_config,
            "melody": adjusted_melody,
            "harmony": harmony,
            "characteristics": self._analyze_section_characteristics(
                adjusted_melody, harmony, section_config
            )
        }
    
    def _adjust_section_melody(self, melody, section_config: SectionConfig,
                             is_theme: bool, is_contrast: bool, is_return: bool):
        """调整段落旋律特性"""
        adjusted_melody = melody.copy()
        
        # A段（主题）：简单、清晰的主题
        if is_theme:
            # 简化节奏，突出主题
            adjusted_melody = self._simplify_melody_rhythm(melody)
            adjusted_melody = self._enhance_melody_clarity(melody)
        
        # B段（对比部）：复杂的和声和节奏
        elif is_contrast:
            # 增加节奏变化，使用更多音程跳跃
            adjusted_melody = self._add_melody_complexity(melody)
            adjusted_melody = self._apply_transposition(melody, section_config.transposition)
        
        # A段再现：加强力度和变化
        elif is_return:
            # 保持主题但有装饰性变化
            adjusted_melody = self._add_melody_variations(melody)
            # 应用力度变化
            adjusted_melody = self._apply_dynamic_variations(melody, section_config.dynamic_level)
        
        return adjusted_melody
    
    def _simplify_melody_rhythm(self, melody):
        """简化旋律节奏，突出主题"""
        # 这里应该实现对旋律的节奏简化
        # 简化：减少过于复杂的节奏，使用更规整的节拍
        return melody  # 简化实现
    
    def _enhance_melody_clarity(self, melody):
        """增强旋律清晰度"""
        # 提高旋律的清晰度，使主题更加突出
        return melody  # 简化实现
    
    def _add_melody_complexity(self, melody):
        """增加旋律复杂度，用于对比段"""
        # 添加更多音程变化，使用非规整节奏
        return melody  # 简化实现
    
    def _apply_transposition(self, melody, transposition_semitones: int):
        """应用移调"""
        if transposition_semitones != 0:
            # 移调整个旋律
            transposed_melody = []
            for note_value, duration in melody.get_note_durations():
                transposed_note = note_value + transposition_semitones
                # 确保音符在合理范围内
                if 21 <= transposed_note <= 108:  # MIDI音符范围
                    transposed_melody.append((transposed_note, duration))
            return transposed_melody
        return melody.get_note_durations()
    
    def _add_melody_variations(self, melody):
        """添加旋律变化，用于再现段"""
        # 在再现主题时添加装饰性变化
        return melody  # 简化实现
    
    def _apply_dynamic_variations(self, melody, dynamic_level: float):
        """应用力度变化"""
        # 根据力度等级调整旋律的力度
        return melody  # 简化实现
    
    def _analyze_section_characteristics(self, melody, harmony, section_config: SectionConfig) -> Dict[str, Any]:
        """分析段落特征"""
        return {
            "emotion": section_config.emotion.value,
            "tempo": section_config.tempo_change,
            "dynamic_level": section_config.dynamic_level,
            "key": self.config.key,
            "transposition": section_config.transposition,
            "melody_characteristics": self._analyze_melody_characteristics(melody),
            "harmony_characteristics": self._analyze_harmony_characteristics(harmony)
        }
    
    def _analyze_melody_characteristics(self, melody) -> Dict[str, Any]:
        """分析旋律特征"""
        return {
            "length": len(melody),
            "pitch_range": self._calculate_pitch_range(melody),
            "rhythmic_variety": self._calculate_rhythmic_variety(melody)
        }
    
    def _analyze_harmony_characteristics(self, harmony) -> Dict[str, Any]:
        """分析和声特征"""
        return {
            "chord_count": len(harmony["chord_progression"]),
            "chord_types": list(set(chord["chord"].chord_type for chord in harmony["chord_progression"]))
        }
    
    def _calculate_pitch_range(self, melody) -> int:
        """计算音域范围"""
        if not melody:
            return 0
        note_values = [note[0] for note in melody]
        return max(note_values) - min(note_values)
    
    def _calculate_rhythmic_variety(self, melody) -> float:
        """计算节奏变化程度"""
        if not melody:
            return 0.0
        
        durations = [note[1] for note in melody]
        unique_durations = len(set(durations))
        return unique_durations / len(durations)
    
    def _generate_transitions(self) -> List[Dict[str, Any]]:
        """生成过渡段"""
        transitions = []
        
        # A到B的过渡
        transition_ab = self._generate_transition_between_sections(
            self.config.a_section, self.config.b_section
        )
        transitions.append({"from": "A", "to": "B", "transition": transition_ab})
        
        # B到A再现的过渡
        transition_ba = self._generate_transition_between_sections(
            self.config.b_section, self.config.return_section
        )
        transitions.append({"from": "B", "to": "A", "transition": transition_ba})
        
        return transitions
    
    def _generate_transition_between_sections(self, from_section: SectionConfig, 
                                           to_section: SectionConfig) -> Dict[str, Any]:
        """生成两个段落之间的过渡"""
        # 使用混合情感和渐变的力度变化
        transition_emotion = self._blend_emotions(from_section.emotion, to_section.emotion)
        
        transition_config = SectionConfig(
            role=SectionRole.BRIDGE,
            length=self.config.transition_length,
            emotion=transition_emotion,
            dynamic_level=(from_section.dynamic_level + to_section.dynamic_level) / 2
        )
        
        # 生成过渡段
        return self._generate_section(transition_config)
    
    def _blend_emotions(self, emotion1: EmotionType, emotion2: EmotionType) -> EmotionType:
        """混合两种情感"""
        # 简单的情感混合逻辑
        if emotion1 == EmotionType.HAPPY and emotion2 == EmotionType.SAD:
            return EmotionType.NEUTRAL
        elif emotion1 == EmotionType.SAD and emotion2 == EmotionType.HAPPY:
            return EmotionType.PEACEFUL
        else:
            return EmotionType.NEUTRAL
    
    def _generate_coda(self) -> Dict[str, Any]:
        """生成尾声"""
        coda_config = SectionConfig(
            role=SectionRole.CODA,
            length=self.config.coda_length,
            emotion=EmotionType.PEACEFUL,
            dynamic_level=0.6,  # 逐渐减弱
            tempo_change=0.8     # 稍微放慢
        )
        
        return self._generate_section(coda_config)
    
    def _calculate_total_measures(self, sections: Dict[str, Any]) -> int:
        """计算总小节数"""
        total = 0
        
        # A段
        if 'a_section' in sections:
            total += sections['a_section']['config'].length
        
        # B段
        if 'b_section' in sections:
            total += sections['b_section']['config'].length
        
        # A段再现
        if 'return_section' in sections:
            total += sections['return_section']['config'].length
        
        # 过渡段
        if 'transitions' in sections:
            for transition in sections['transitions']:
                total += transition['transition']['config'].length
        
        # 尾声
        if 'coda' in sections:
            total += sections['coda']['config'].length
        
        return total
    
    def _generate_complete_midi(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """生成完整的MIDI数据"""
        # 这里应该实现将所有段落组合成完整的MIDI文件
        # 暂时返回结构信息
        return {
            "tracks": ["melody", "harmony", "bass", "rhythm"],
            "total_duration": self._calculate_total_measures(sections) * 4,  # 转换为拍数
            "key_signature": self.config.key,
            "time_signature": self.config.time_signature
        }


class FormAnalyzer:
    """曲式分析器"""
    
    @staticmethod
    def analyze_form(midi_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析MIDI数据的曲式结构"""
        # 这里应该实现曲式分析算法
        return {
            "detected_form": "ABA",
            "confidence": 0.85,
            "sections": ["A", "B", "A"],
            "characteristics": {
                "contrast": "moderate",
                "development": "limited",
                "recapitulation": "strong"
            }
        }