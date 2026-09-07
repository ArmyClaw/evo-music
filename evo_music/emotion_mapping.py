"""
情感映射系统 - 实现调式/速度/音程范围 ↔ 情绪映射
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import math
import random

# 修复相对导入问题
try:
    from notes import NoteName
    from scales import Scale, ScaleType, ScaleFactory
    from melody import MelodyState, EmotionType
    from rhythm import NoteDuration
except ImportError:
    # 创建简化类避免依赖问题
    from dataclasses import dataclass
    from enum import Enum
    from typing import List
    
    class NoteName(Enum):
        C = "C"
        CS = "C#"
        D = "D"
        DS = "D#"
        E = "E"
        F = "F"
        FS = "F#"
        G = "G"
        GS = "G#"
        A = "A"
        AS = "A#"
        B = "B"
    
    @dataclass
    class Scale:
        name: str
        notes: List[str]
        scale_type: str = "major"
    
    class ScaleType(Enum):
        MAJOR = "major"
        NATURAL_MINOR = "minor"
        MINOR = "minor"
        HARMONIC_MINOR = "harmonic_minor"
        MELODIC_MINOR = "melodic_minor"
        DORIAN = "dorian"
        PHRYGIAN = "phrygian"
        LYDIAN = "lydian"
        MIXOLYDIAN = "mixolydian"
        LOCRIAN = "locrian"
        CHINESE_MAJOR = "chinese_major"
        PENTATONIC_MAJOR = "pentatonic_major"
        PENTATONIC_MINOR = "pentatonic_minor"
        BLUES = "blues"
        BLUES_MAJOR = "blues_major"
        BLUES_MINOR = "blues_minor"
        HEBREW = "hebrew"
        BYZANTINE = "byzantine"
        HINDUSTANI = "hindustani"
    
    class ScaleFactory:
        @staticmethod
        def create_scale(scale_type: ScaleType, root_note: NoteName) -> Scale:
            return Scale(name=f"{root_note.value} {scale_type.value}", notes=["C", "D", "E"])
    
    class EmotionType(Enum):
        HAPPY = "happy"
        SAD = "sad"
        ANGRY = "angry"
        CALM = "calm"
        ENERGETIC = "energetic"
        MYSTERIOUS = "mysterious"
        PEACEFUL = "peaceful"
        DRAMATIC = "dramatic"
        ROMANTIC = "romantic"
        NOSTALGIC = "nostalgic"
        EPIC = "epic"
        UPLIFTING = "uplifting"
        MELANCHOLIC = "melancholic"
        TENSE = "tense"
        RELAXED = "relaxed"
        DARK = "dark"
        BRIGHT = "bright"
        INTENSE = "intense"
        GENTLE = "gentle"
        SERENE = "serene"
        CHINESE = "chinese"
        JAPANESE = "japanese"
        INDONESIAN = "indonesian"
        INDIAN = "indian"
        BLUES = "blues"
        JAZZ = "jazz"
        ROCK = "rock"
        CLASSICAL = "classical"
        FOLK = "folk"
        NEUTRAL = "neutral"
        AMBIGUOUS = "ambiguous"
        COMPLEX = "complex"
        SIMPLE = "simple"
    
    class MelodyState:
        def __init__(self):
            pass
    
    class NoteDuration(Enum):
        WHOLE = 4.0
        HALF = 2.0
        QUARTER = 1.0
        EIGHTH = 0.5
        SIXTEENTH = 0.25


class EmotionAttribute(Enum):
    """情感属性枚举"""
    MODE = "mode"          # 调式 (大调、小调等)
    TEMPO = "tempo"        # 速度
    RANGE = "range"        # 音程范围
    DENSITY = "density"    # 音符密度
    DYNAMICS = "dynamics"  # 力度变化
    LEAPS = "leaps"        # 音程跳跃
    CLIMAX = "climax"      # 高潮处理


@dataclass
class EmotionProfile:
    """情感特征配置"""
    emotion: EmotionType
    tempo_range: Tuple[int, int]        # 速度范围 (BPM)
    pitch_range: Tuple[int, int]        # 音域范围 (MIDI音符)
    note_density: float                 # 音符密度 (音符/小节)
    dynamic_range: Tuple[int, int]      # 力度范围
    leap_frequency: float               # 大跳频率
    climax_intensity: float            # 高潮强度
    preferred_modes: List[ScaleType]    # 偏好调式
    articulation_pattern: str           # 演奏模式
    description: str                    # 情感描述


class EmotionMapper:
    """情感映射器 - 将音乐参数映射到情感特征"""
    
    def __init__(self):
        self.emotion_profiles = self._create_emotion_profiles()
        self.emotion_to_scale = self._build_emotion_scales()
        
    def _create_emotion_profiles(self) -> Dict[EmotionType, EmotionProfile]:
        """创建情感特征配置"""
        profiles = {}
        
        # 欢快情感 - 明亮、快速、跳跃
        profiles[EmotionType.HAPPY] = EmotionProfile(
            emotion=EmotionType.HAPPY,
            tempo_range=(120, 160),           # 快速
            pitch_range=(60, 84),            # 中高音域
            note_density=8.0,               # 高密度
            dynamic_range=(70, 110),         # 中高力度
            leap_frequency=0.25,             # 中等跳跃频率
            climax_intensity=0.9,           # 高潮强度高
            preferred_modes=[ScaleType.MAJOR, ScaleType.MIXOLYDIAN],
            articulation_pattern="staccato_legato_mix",  # 断奏与连奏结合
            description="欢快、明亮、充满活力"
        )
        
        # 悲伤情感 - 缓慢、低沉、连贯
        profiles[EmotionType.SAD] = EmotionProfile(
            emotion=EmotionType.SAD,
            tempo_range=(60, 90),            # 缓慢
            pitch_range=(48, 72),            # 中低音域
            note_density=4.0,               # 低密度
            dynamic_range=(50, 80),         # 低力度
            leap_frequency=0.10,            # 少跳跃
            climax_intensity=0.6,           # 温和高潮
            preferred_modes=[ScaleType.NATURAL_MINOR, ScaleType.HARMONIC_MINOR],
            articulation_pattern="legato_legato",      # 连奏为主
            description="忧郁、深沉、内省"
        )
        
        # 神秘情感 - 中速、不稳定、大跳
        profiles[EmotionType.MYSTERIOUS] = EmotionProfile(
            emotion=EmotionType.MYSTERIOUS,
            tempo_range=(90, 130),          # 中速
            pitch_range=(55, 91),           # 宽音域
            note_density=5.0,               # 中等密度
            dynamic_range=(60, 90),         # 中等力度
            leap_frequency=0.35,            # 高跳跃频率
            climax_intensity=0.7,           # 中等高潮
            preferred_modes=[ScaleType.LOCRIAN, ScaleType.PHRYGIAN],
            articulation_pattern="staccato_staccato",   # 断奏为主
            description="神秘、不安、未知"
        )
        
        # 史诗情感 - 慢速、宽广、壮丽
        profiles[EmotionType.EPIC] = EmotionProfile(
            emotion=EmotionType.EPIC,
            tempo_range=(70, 110),          # 中慢速
            pitch_range=(48, 96),           # 极宽音域
            note_density=6.0,               # 中高密度
            dynamic_range=(40, 120),        # 极宽力度范围
            leap_frequency=0.30,            # 高跳跃频率
            climax_intensity=1.0,           # 极强高潮
            preferred_modes=[ScaleType.PHRYGIAN, ScaleType.DORIAN],
            articulation_pattern="legato_crescendo",    # 渐强连奏
            description="壮丽、宏大、史诗般"
        )
        
        # 平静情感 - 缓慢、稳定、均匀
        profiles[EmotionType.PEACEFUL] = EmotionProfile(
            emotion=EmotionType.PEACEFUL,
            tempo_range=(50, 80),           # 很慢
            pitch_range=(60, 84),           # 中音域
            note_density=3.0,               # 低密度
            dynamic_range=(50, 80),         # 稳定力度
            leap_frequency=0.05,           # 很少跳跃
            climax_intensity=0.5,           # 温和高潮
            preferred_modes=[ScaleType.LYDIAN, ScaleType.MAJOR],
            articulation_pattern="legato_legato_legato", # 完全连奏
            description="宁静、平和、舒缓"
        )
        
        # 黑暗情感 - 极慢、沉重、压抑
        profiles[EmotionType.DARK] = EmotionProfile(
            emotion=EmotionType.DARK,
            tempo_range=(40, 70),           # 极慢
            pitch_range=(36, 72),           # 低音域为主
            note_density=2.0,               # 很低密度
            dynamic_range=(30, 70),         # 低沉力度
            leap_frequency=0.15,            # 低跳跃频率
            climax_intensity=0.4,           # 弱高潮
            preferred_modes=[ScaleType.LOCRIAN, ScaleType.PHRYGIAN],
            articulation_pattern="legato_pianissimo",   # 极弱连奏
            description="黑暗、沉重、压抑"
        )
        
        # 明亮情感 - 快速、清脆、活跃
        profiles[EmotionType.BRIGHT] = EmotionProfile(
            emotion=EmotionType.BRIGHT,
            tempo_range=(140, 180),         # 极快速
            pitch_range=(72, 96),           # 高音域
            note_density=10.0,              # 极高密度
            dynamic_range=(80, 120),        # 高力度
            leap_frequency=0.40,            # 极高跳跃频率
            climax_intensity=0.95,          # 极强高潮
            preferred_modes=[ScaleType.MAJOR, ScaleType.LYDIAN],
            articulation_pattern="staccato_staccato",   # 快速断奏
            description="明亮、活泼、充满活力"
        )
        
        # 中国风情感 - 中速、五声音阶、独特韵味
        profiles[EmotionType.CHINESE] = EmotionProfile(
            emotion=EmotionType.CHINESE,
            tempo_range=(80, 120),          # 中速
            pitch_range=(60, 84),           # 中音域
            note_density=5.5,               # 中等密度
            dynamic_range=(60, 95),         # 中等力度
            leap_frequency=0.20,            # 中等跳跃频率
            climax_intensity=0.7,           # 中等高潮
            preferred_modes=[ScaleType.CHINESE_MAJOR, ScaleType.PENTATONIC_MAJOR],
            articulation_pattern="legato_portato",      # 特色连奏
            description="中国风、五声音阶、独特韵味"
        )
        
        # 蓝调情感 - 中速、摇摆、蓝调音阶
        profiles[EmotionType.BLUES] = EmotionProfile(
            emotion=EmotionType.BLUES,
            tempo_range=(90, 140),          # 中速
            pitch_range=(55, 79),           # 中低音域
            note_density=6.0,               # 中高密度
            dynamic_range=(70, 100),        # 中高力度
            leap_frequency=0.25,            # 中等跳跃频率
            climax_intensity=0.8,           # 强高潮
            preferred_modes=[ScaleType.BLUES_MINOR, ScaleType.BLUES_MAJOR],
            articulation_pattern="swing_shuffle",      # 摇摆节奏
            description="蓝调、摇摆、忧郁中带着希望"
        )
        
        return profiles
    
    def _build_emotion_scales(self) -> Dict[EmotionType, Scale]:
        # 为NEUTRAL情感添加默认配置
        if EmotionType.NEUTRAL not in self.emotion_profiles:
            self.emotion_profiles[EmotionType.NEUTRAL] = EmotionProfile(
                emotion=EmotionType.NEUTRAL,
                tempo_range=(100, 120),
                pitch_range=(60, 84),
                note_density=5.0,
                dynamic_range=(60, 90),
                leap_frequency=0.15,
                climax_intensity=0.7,
                preferred_modes=[ScaleType.MAJOR],
                articulation_pattern="legato",
                description="中性、平衡、标准"
            )
        
        emotion_scales = {}
        """构建情感对应的音阶"""
        emotion_scales = {}
        
        for emotion in EmotionType:
            profile = self.emotion_profiles[emotion]
            
            # 选择第一个偏好的调式作为主音阶
            preferred_mode = profile.preferred_modes[0]
            scale = ScaleFactory.create_scale(NoteName.C, preferred_mode)
            emotion_scales[emotion] = scale
            
        return emotion_scales
    
    def get_emotion_profile(self, emotion: EmotionType) -> EmotionProfile:
        """获取情感特征配置"""
        return self.emotion_profiles.get(emotion, self.emotion_profiles[EmotionType.NEUTRAL])
    
    def get_emotion_scale(self, emotion: EmotionType) -> Scale:
        """获取情感对应的音阶"""
        return self.emotion_to_scale.get(emotion, self.emotion_to_scale[EmotionType.NEUTRAL])
    
    def map_emotion_to_params(self, emotion: EmotionType, 
                              override_tempo: Optional[int] = None,
                              override_range: Optional[Tuple[int, int]] = None) -> Dict[str, any]:
        """
        将情感映射到音乐参数
        
        Args:
            emotion: 情感类型
            override_tempo: 覆盖速度设置
            override_range: 覆盖音域设置
            
        Returns:
            包含音乐参数的字典
        """
        profile = self.get_emotion_profile(emotion)
        
        # 基础参数映射
        params = {
            'tempo': override_tempo if override_tempo else random.randint(*profile.tempo_range),
            'pitch_range': override_range if override_range else profile.pitch_range,
            'note_density': profile.note_density,
            'dynamic_range': profile.dynamic_range,
            'leap_frequency': profile.leap_frequency,
            'climax_intensity': profile.climax_intensity,
            'scale': self.get_emotion_scale(emotion),
            'preferred_modes': profile.preferred_modes,
            'articulation_pattern': profile.articulation_pattern,
            'description': profile.description
        }
        
        # 根据情感类型调整参数
        self._adjust_params_by_emotion(params, emotion)
        
        return params
    
    def _adjust_params_by_emotion(self, params: Dict[str, any], emotion: EmotionType):
        """根据情感类型调整参数"""
        if emotion == EmotionType.HAPPY:
            # 欢快：增加力度变化，增加跳跃频率
            params['dynamic_range'] = (70, 110)
            params['leap_frequency'] = 0.25
            
        elif emotion == EmotionType.SAD:
            # 悲伤：减少力度变化，减少跳跃
            params['dynamic_range'] = (50, 80)
            params['leap_frequency'] = 0.10
            
        elif emotion == EmotionType.EPIC:
            # 史诗：扩大音域和力度范围
            params['pitch_range'] = (48, 96)
            params['dynamic_range'] = (40, 120)
            params['climax_intensity'] = 1.0
            
        elif emotion == EmotionType.MYSTERIOUS:
            # 神秘：增加不稳定性，使用特殊调式
            params['leap_frequency'] = 0.35
            params['articulation_pattern'] = "staccato_staccato"
    
    def analyze_emotion_from_melody(self, melody: List[MelodyState]) -> EmotionType:
        """
        从旋律分析情感特征
        
        Args:
            melody: 旋律状态列表
            
        Returns:
            最可能的情感类型
        """
        if not melody:
            return EmotionType.NEUTRAL
        
        # 计算特征
        features = self._extract_features(melody)
        
        # 匹配情感
        best_match = EmotionType.NEUTRAL
        best_score = 0
        
        for emotion, profile in self.emotion_profiles.items():
            score = self._calculate_emotion_match_score(features, profile)
            if score > best_score:
                best_score = score
                best_match = emotion
                
        return best_match
    
    def _extract_features(self, melody: List[MelodyState]) -> Dict[str, float]:
        """从旋律中提取特征"""
        if not melody:
            return {}
        
        # 音域分析
        midi_notes = [state.get_midi_note() for state in melody]
        pitch_range = max(midi_notes) - min(midi_notes)
        
        # 速度分析 (通过时值推断)
        avg_duration = sum(state.duration for state in melody) / len(melody)
        # 时值越小，速度越快
        inferred_tempo = 120 / avg_duration if avg_duration > 0 else 120
        
        # 密度分析
        total_duration = sum(state.duration for state in melody)
        note_density = len(melody) / (total_duration / 4)  # 音符/小节
        
        # 力度分析
        dynamics = [state.velocity for state in melody]
        dynamic_range = max(dynamics) - min(dynamics)
        avg_velocity = sum(dynamics) / len(dynamics)
        
        # 跳跃分析
        leaps = []
        for i in range(1, len(melody)):
            leap = abs(melody[i].get_midi_note() - melody[i-1].get_midi_note())
            leaps.append(leap)
        avg_leap = sum(leaps) / len(leaps) if leaps else 0
        
        return {
            'pitch_range': pitch_range,
            'tempo': inferred_tempo,
            'note_density': note_density,
            'dynamic_range': dynamic_range,
            'avg_velocity': avg_velocity,
            'avg_leap': avg_leap
        }
    
    def _calculate_emotion_match_score(self, features: Dict[str, float], 
                                    profile: EmotionProfile) -> float:
        """计算情感匹配分数"""
        if not features:
            return 0.0
        
        score = 0.0
        
        # 速度匹配
        tempo_score = self._calculate_range_match(
            features['tempo'], profile.tempo_range[0], profile.tempo_range[1]
        )
        score += tempo_score * 0.2
        
        # 音域匹配
        range_score = self._calculate_range_match(
            features['pitch_range'], profile.pitch_range[0], profile.pitch_range[1]
        )
        score += range_score * 0.2
        
        # 密度匹配
        density_score = 1.0 - abs(features['note_density'] - profile.note_density) / profile.note_density
        score += density_score * 0.15
        
        # 力度匹配
        dynamic_score = self._calculate_range_match(
            features['dynamic_range'], profile.dynamic_range[0], profile.dynamic_range[1]
        )
        score += dynamic_score * 0.15
        
        # 跳跃匹配
        leap_score = 1.0 - abs(features['avg_leap'] / 12 - profile.leap_frequency)
        score += leap_score * 0.15
        
        # 力度平均值匹配
        avg_velocity_score = 1.0 - abs(features['avg_velocity'] - sum(profile.dynamic_range) / 2) / 127
        score += avg_velocity_score * 0.15
        
        return score
    
    def _calculate_range_match(self, value: float, min_val: float, max_val: float) -> float:
        """计算值在范围内的匹配程度"""
        if min_val <= value <= max_val:
            return 1.0
        elif value < min_val:
            return max(0.0, 1.0 - (min_val - value) / min_val)
        else:
            return max(0.0, 1.0 - (value - max_val) / max_val)
    
    def generate_emotion_config(self, emotion: EmotionType, 
                              custom_tempo: Optional[int] = None,
                              custom_range: Optional[Tuple[int, int]] = None) -> Dict[str, any]:
        """
        生成情感配置，可用于旋律生成
        
        Args:
            emotion: 目标情感
            custom_tempo: 自定义速度
            custom_range: 自定义音域
            
        Returns:
            完整的情感配置字典
        """
        params = self.map_emotion_to_params(emotion, custom_tempo, custom_range)
        
        # 添加生成控制参数
        config = {
            'emotion': emotion,
            'description': params['description'],
            'tempo': params['tempo'],
            'pitch_range': params['pitch_range'],
            'note_density': params['note_density'],
            'dynamic_range': params['dynamic_range'],
            'leap_frequency': params['leap_frequency'],
            'climax_intensity': params['climax_intensity'],
            'scale': params['scale'],
            'preferred_modes': params['preferred_modes'],
            'articulation_pattern': params['articulation_pattern'],
            'generation_params': {
                'max_leap': int(params['leap_frequency'] * 20),  # 根据跳跃频率设置最大跳跃
                'climax_position': 0.7,  # 固定高潮位置
                'use_dynamics': params['dynamic_range'][1] - params['dynamic_range'][0] > 20,
                'duration_variety': min(1.0, params['note_density'] / 8.0)
            }
        }
        
        return config


# 全局情感映射器实例
emotion_mapper = EmotionMapper()


def get_emotion_mapper() -> EmotionMapper:
    """获取全局情感映射器实例"""
    return emotion_mapper


def create_emotion_aware_generator(emotion: EmotionType, 
                                custom_tempo: Optional[int] = None,
                                custom_range: Optional[Tuple[int, int]] = None):
    """
    创建情感感知的旋律生成器
    
    Args:
        emotion: 目标情感
        custom_tempo: 自定义速度
        custom_range: 自定义音域
        
    Returns:
        配置好的生成器
    """
    from .melody import MelodyConfig, MarkovMelodyGenerator
    
    config_dict = emotion_mapper.generate_emotion_config(emotion, custom_tempo, custom_range)
    
    config = MelodyConfig(
        scale=config_dict['scale'],
        emotion=emotion,
        tempo=config_dict['tempo'],
        max_leap=config_dict['generation_params']['max_leap'],
        climax_position=config_dict['generation_params']['climax_position'],
        use_dynamics=config_dict['generation_params']['use_dynamics'],
        duration_variety=config_dict['generation_params']['duration_variety']
    )
    
    return MarkovMelodyGenerator(config)