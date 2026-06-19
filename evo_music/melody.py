"""
旋律生成系统 - 基于马尔可夫链的旋律生成算法
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import random
from collections import defaultdict
import math

from .notes import NoteName
from .scales import Scale, ScaleType
from .scales import ScaleFactory
from .rhythm import NoteDuration
from .melody_optimizer import MelodyOptimizer, HarmonyOptimizer


class EmotionType(Enum):
    """情感类型"""
    HAPPY = "happy"
    SAD = "sad"
    MYSTERIOUS = "mysterious"
    EPIC = "epic"
    PEACEFUL = "peaceful"
    DARK = "dark"
    BRIGHT = "bright"
    CHINESE = "chinese"
    BLUES = "blues"
    NEUTRAL = "neutral"


@dataclass
class MelodyConfig:
    """旋律生成配置"""
    scale: Scale                           # 音阶
    emotion: EmotionType = EmotionType.NEUTRAL  # 情感
    length: int = 32                       # 旋律长度
    start_note: NoteName = NoteName.C      # 起始音符
    start_octave: int = 4                  # 起始八度
    tempo: int = 120                       # 速度
    max_leap: int = 7                      # 最大音程跳跃
    climax_position: float = 0.7           # 高潮位置
    use_dynamics: bool = True              # 使用力度变化
    duration_variety: float = 0.7          # 时值变化程度
    enable_optimization: bool = True      # 启用旋律优化
    use_harmony_optimization: bool = False  # 使用和声优化
    smooth_transitions: bool = True       # 平滑音程过渡
    emotion_consistency: bool = True       # 情感一致性


@dataclass
class MelodyState:
    """旋律状态"""
    note: NoteName                         # 当前音符
    octave: int                            # 八度
    duration: float                        # 音符时值
    velocity: int                          # 力度 (0-127)
    time_position: float                    # 时间位置（小节数）
    
    def get_midi_note(self) -> int:
        """获取MIDI音符编号"""
        return self.note.value + self.octave * 12 + 60  # 60 = C3


class TransitionMatrix:
    """音程转换概率矩阵"""
    
    def __init__(self, scale: Scale):
        self.scale = scale
        self.note_probabilities = self._build_note_matrix()
        self.duration_probabilities = self._build_duration_matrix()
        
    def _build_note_matrix(self) -> Dict[Tuple[int, int], float]:
        """构建音符转移概率矩阵"""
        matrix = defaultdict(float)
        scale_notes = [note.value for note in self.scale.notes]
        
        # 基础概率：倾向于相邻音阶内的音符
        for i, from_note in enumerate(scale_notes):
            for j, to_note in enumerate(scale_notes):
                # 相邻音符有更高概率
                distance = abs(i - j)
                if distance == 0:
                    probability = 0.1  # 重复音符
                elif distance == 1:
                    probability = 0.4  # 相邻音符
                elif distance == 2:
                    probability = 0.3  # 小跳
                else:
                    probability = 0.2 / distance  # 大跳
                    
                matrix[(from_note, to_note)] = probability
        
        # 归一化
        total = sum(matrix.values())
        for key in matrix:
            matrix[key] /= total
            
        return dict(matrix)
    
    def _build_duration_matrix(self) -> Dict[float, float]:
        """构建时值转移概率矩阵"""
        durations = [0.25, 0.5, 1.0, 2.0, 4.0]  # 十六分到全音符
        
        matrix = {}
        for i, duration in enumerate(durations):
            # 时值倾向于交替使用
            if i > 0:
                matrix[duration] = 0.6 if i % 2 == 0 else 0.4
            else:
                matrix[duration] = 0.5
                
        # 归一化
        total = sum(matrix.values())
        for duration in matrix:
            matrix[duration] /= total
            
        return matrix
    
    def get_next_note(self, current_note: int) -> int:
        """根据当前音符获取下一个音符"""
        candidates = []
        total_prob = 0
        
        # 根据音阶约束过滤候选音符
        scale_notes = [note.value for note in self.scale.notes]
        
        for (from_note, to_note), prob in self.note_probabilities.items():
            if from_note == current_note and to_note in scale_notes:
                candidates.append((to_note, prob))
                total_prob += prob
        
        if not candidates:
            # 如果没有候选，使用随机音阶内音符
            return random.choice(scale_notes)
            
        # 按概率选择
        rand = random.random() * total_prob
        cumulative = 0
        
        for note, prob in candidates:
            cumulative += prob
            if rand <= cumulative:
                return note
                
        return candidates[-1][0]
    
    def get_next_duration(self, current_duration: float) -> float:
        """获取下一个音符时值"""
        candidates = []
        total_prob = 0
        
        for duration, prob in self.duration_probabilities.items():
            candidates.append((duration, prob))
            total_prob += prob
            
        rand = random.random() * total_prob
        cumulative = 0
        
        for duration, prob in candidates:
            cumulative += prob
            if rand <= cumulative:
                return duration
                
        return current_duration


class MarkovMelodyGenerator:
    """马尔可夫链旋律生成器"""
    
    def __init__(self, config: MelodyConfig):
        self.config = config
        self.transition_matrix = TransitionMatrix(config.scale)
        self.sequence: List[MelodyState] = []
        self.current_state: Optional[MelodyState] = None
        
    def generate(self) -> List[MelodyState]:
        """生成旋律序列"""
        self.sequence = []
        self.current_state = MelodyState(
            note=self.config.start_note,
            octave=self.config.start_octave,
            duration=1.0,  # 开始用四分音符
            velocity=80,
            time_position=0.0
        )
        
        self.sequence.append(self.current_state)
        
        for i in range(1, self.config.length):
            self._generate_step(i)
            
        # 应用优化
        self._optimize_melody()
        
        return self.sequence
    
    def _generate_step(self, step: int):
        """生成单个步骤"""
        current_note_value = self.current_state.note.value
        
        # 获取下一个音符
        next_note_value = self.transition_matrix.get_next_note(current_note_value)
        next_note = NoteName(next_note_value)
        
        # 控制八度跳跃
        next_octave = self._calculate_octave(current_note_value, next_note_value, step)
        
        # 获取下一个时值
        next_duration = self.transition_matrix.get_next_duration(self.current_state.duration)
        
        # 计算力度
        next_velocity = self._calculate_velocity(step)
        
        # 更新状态
        self.current_state = MelodyState(
            note=next_note,
            octave=next_octave,
            duration=next_duration,
            velocity=next_velocity,
            time_position=step
        )
        
        self.sequence.append(self.current_state)
    
    def _calculate_octave(self, current_note: int, next_note: int, step: int) -> int:
        """计算八度位置"""
        base_octave = self.config.start_octave
        
        # 基于高潮位置的八度变化
        climax_step = int(self.config.length * self.config.climax_position)
        
        if abs(step - climax_step) < 3:  # 高潮附近
            # 高潮时适当提高八度
            if next_note > current_note:
                return base_octave + 1
            else:
                return base_octave
        
        # 限制最大跳跃
        leap = abs(next_note - current_note)
        if leap > self.config.max_leap:
            # 大跳时降低八度
            return base_octave - 1
        
        return base_octave
    
    def _calculate_velocity(self, step: int) -> int:
        """计算力度"""
        if not self.config.use_dynamics:
            return 80
            
        base_velocity = 80
        climax_step = int(self.config.length * self.config.climax_position)
        
        # 高潮附近力度增强
        if abs(step - climax_step) < 5:
            intensity = 1 - abs(step - climax_step) / 5
            return min(127, int(base_velocity + intensity * 40))
        
        # 随机变化
        return max(40, min(100, base_velocity + random.randint(-20, 20)))
    
    def _optimize_melody(self):
        """优化旋律连贯性 - 使用新的优化器"""
        if not self.config.enable_optimization:
            return
        
        # 创建优化器
        melody_optimizer = MelodyOptimizer(self.config.scale, self.config.max_leap)
        
        # 应用优化
        self.sequence = melody_optimizer.optimize_sequence(self.sequence)
        
        # 如果启用和声优化，应用和声优化
        if self.config.use_harmony_optimization:
            harmony_optimizer = HarmonyOptimizer(self.config.scale)
            # 简单的I-IV-V和弦进行
            chord_progression = [0, 5, 7, 0]  # C-F-G-C
            self.sequence = harmony_optimizer.optimize_for_harmony(self.sequence, chord_progression)
    
    def _find_closest_note(self, target: int, reference: int) -> NoteName:
        """寻找最近的音阶内音符"""
        scale_notes = self.config.scale.notes
        closest_note = None
        min_distance = float('inf')
        
        for note in scale_notes:
            distance = abs(note.value - reference)
            if distance < min_distance:
                min_distance = distance
                closest_note = note
                
        return closest_note


class MelodyTrainer:
    """旋律训练器 - 从现有旋律学习转换模式"""
    
    def __init__(self):
        self.note_transitions = defaultdict(int)
        self.duration_transitions = defaultdict(int)
        self.emotion_patterns = defaultdict(lambda: defaultdict(int))
        
    def train_from_notes(self, melody: List[NoteName], emotion: EmotionType = EmotionType.NEUTRAL):
        """从音符序列训练"""
        for i in range(len(melody) - 1):
            current = melody[i].value
            next_note = melody[i + 1].value
            self.note_transitions[(current, next_note)] += 1
            
        self.emotion_patterns[emotion]['note_patterns'] = dict(self.note_transitions)
    
    def build_emotion_scales(self) -> Dict[EmotionType, Scale]:
        """为不同情感构建音阶"""
        emotion_scales = {}
        
        for emotion in EmotionType:
            if emotion == EmotionType.HAPPY:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.MAJOR)
            elif emotion == EmotionType.SAD:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.NATURAL_MINOR)
            elif emotion == EmotionType.MYSTERIOUS:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.LOCRIAN)
            elif emotion == EmotionType.EPIC:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.PHRYGIAN)
            elif emotion == EmotionType.PEACEFUL:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.LYDIAN)
            elif emotion == EmotionType.DARK:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.HARMONIC_MINOR)
            elif emotion == EmotionType.BRIGHT:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.MAJOR)
            elif emotion == EmotionType.CHINESE:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.CHINESE_MAJOR)
            elif emotion == EmotionType.BLUES:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.BLUES_MINOR)
            else:
                scale = ScaleFactory.create_scale(NoteName.C, ScaleType.MAJOR)
                
            emotion_scales[emotion] = scale
            
        return emotion_scales


# 便利函数
def generate_melody(emotion: str = "happy", length: int = 32, 
                   start_note: str = "C", enable_optimization: bool = True,
                   use_harmony_optimization: bool = False, smooth_transitions: bool = True) -> List[MelodyState]:
    """快速生成旋律的便利函数
    
    Args:
        emotion: 情感类型 (happy, sad, mysterious, epic, peaceful, dark, bright, chinese, blues)
        length: 旋律长度
        start_note: 起始音符
        enable_optimization: 是否启用旋律优化
        use_harmony_optimization: 是否使用和声优化
        smooth_transitions: 是否使用平滑过渡
    """
    
    # 解析情感
    emotion_map = {
        "happy": EmotionType.HAPPY,
        "sad": EmotionType.SAD,
        "mysterious": EmotionType.MYSTERIOUS,
        "epic": EmotionType.EPIC,
        "peaceful": EmotionType.PEACEFUL,
        "dark": EmotionType.DARK,
        "bright": EmotionType.BRIGHT,
        "chinese": EmotionType.CHINESE,
        "blues": EmotionType.BLUES
    }
    
    emotion_type = emotion_map.get(emotion.lower(), EmotionType.NEUTRAL)
    start_note_obj = NoteName.from_string(start_note)
    
    # 获取情感音阶
    trainer = MelodyTrainer()
    emotion_scales = trainer.build_emotion_scales()
    scale = emotion_scales[emotion_type]
    
    # 配置和生成
    config = MelodyConfig(
        scale=scale,
        emotion=emotion_type,
        length=length,
        start_note=start_note_obj,
        enable_optimization=enable_optimization,
        use_harmony_optimization=use_harmony_optimization,
        smooth_transitions=smooth_transitions,
        emotion_consistency=True
    )
    
    generator = MarkovMelodyGenerator(config)
    return generator.generate()