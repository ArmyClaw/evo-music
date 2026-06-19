"""
旋律连贯性优化模块
专门用于优化旋律的流畅性和连贯性，避免不协和跳跃
"""

from typing import List, Dict, Tuple, Optional
import random
from .notes import NoteName
from .scales import Scale
from dataclasses import dataclass

@dataclass
class OptimizedMelodyState:
    """优化的旋律状态（简化版）"""
    note: NoteName                         # 当前音符
    octave: int                            # 八度
    duration: float                        # 音符时值
    velocity: int                          # 力度 (0-127)
    time_position: float                    # 时间位置（小节数）

    def get_midi_note(self) -> int:
        """获取MIDI音符编号"""
        return self.note.value + self.octave * 12 + 60  # 60 = C3


class EmotionType:
    """情感类型（简化版）"""
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


class MelodyOptimizer:
    """旋律优化器 - 专门处理旋律连贯性"""
    
    def __init__(self, scale: Scale, max_leap: int = 7):
        self.scale = scale
        self.max_leap = max_leap
        self.smooth_transition_threshold = 3  # 平滑转换阈值
        self.preferred_directions = {}  # 首选方向
        
    def optimize_sequence(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """优化整个旋律序列"""
        optimized = melody.copy()
        
        # 第一阶段：修复大跳
        optimized = self._fix_large_jumps(optimized)
        
        # 第二阶段：平滑音程过渡
        optimized = self._smooth_intervals(optimized)
        
        # 第三阶段：优化节奏模式
        optimized = self._optimize_rhythm_patterns(optimized)
        
        # 第四阶段：情感一致性优化
        optimized = self._apply_emotion_consistency(optimized)
        
        # 第五阶段：高潮增强
        optimized = self._enhance_climax(optimized)
        
        return optimized
    
    def _fix_large_jumps(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """修复不协和的大跳"""
        scale_notes_values = [note.value for note in self.scale.notes]
        
        for i in range(1, len(melody)):
            prev = melody[i-1]
            curr = melody[i]
            
            # 计算音程距离
            leap = abs(curr.note.value - prev.note.value)
            
            if leap > self.max_leap:
                # 找到最近的平滑替代音符
                replacement = self._find_smooth_transition(prev.note.value, curr.note.value, scale_notes_values)
                if replacement:
                    curr.note = NoteName(replacement)
                    
        return melody
    
    def _find_smooth_transition(self, from_note: int, to_note: int, scale_notes: List[int]) -> Optional[int]:
        """寻找平滑的过渡音符"""
        
        # 如果目标音在音阶内，直接返回
        if to_note in scale_notes:
            return to_note
        
        # 寻找最近的音阶内音符
        closest_note = None
        min_distance = float('inf')
        
        for scale_note in scale_notes:
            distance = abs(scale_note - to_note)
            if distance < min_distance:
                min_distance = distance
                closest_note = scale_note
        
        # 检查是否过远
        if min_distance <= self.max_leap:
            return closest_note
        else:
            # 找到中间的过渡音符
            direction = 1 if to_note > from_note else -1
            mid_note = from_note + direction * (self.max_leap // 2)
            
            # 找到音阶内最接近的中间音符
            for scale_note in scale_notes:
                if abs(scale_note - mid_note) <= 1:
                    return scale_note
            
            return closest_note
    
    def _smooth_intervals(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """平滑音程过渡"""
        
        for i in range(1, len(melody)):
            prev = melody[i-1]
            curr = melody[i]
            
            # 计算当前音程
            interval = curr.note.value - prev.note.value
            
            # 如果是较大的音程，添加过渡音符
            if abs(interval) >= self.smooth_transition_threshold:
                melody = self._add_transition_notes(melody, i-1, i)
        
        return melody
    
    def _add_transition_notes(self, melody: List[OptimizedMelodyState], from_idx: int, to_idx: int) -> List[OptimizedMelodyState]:
        """在两个音符之间添加过渡音符"""
        if to_idx - from_idx <= 1:
            return melody
        
        from_note = melody[from_idx].note.value
        to_note = melody[to_idx].note.value
        
        # 确定过渡方向
        direction = 1 if to_note > from_note else -1
        interval = abs(to_note - from_note)
        
        # 计算需要的过渡音符数量
        transition_count = min(2, interval - 1)  # 最多2个过渡音符
        
        if transition_count <= 0:
            return melody
        
        # 生成过渡音符
        transition_notes = []
        step = interval / (transition_count + 1)
        
        for j in range(1, transition_count + 1):
            target_note = from_note + direction * int(step * j)
            
            # 找到音阶内最接近的音符
            scale_notes = [note.value for note in self.scale.notes]
            closest_note = min(scale_notes, key=lambda x: abs(x - target_note))
            
            transition_notes.append(closest_note)
        
        # 插入过渡音符
        new_melody = melody[:to_idx]
        for j, note_value in enumerate(transition_notes):
            # 复制前一个音符的属性，只改变音符值
            prev_state = melody[to_idx - 1] if j == 0 else new_melody[-1]
            new_note = OptimizedMelodyState(
                note=NoteName(note_value),
                octave=prev_state.octave,
                duration=prev_state.duration * 0.7,  # 过渡音符稍短
                velocity=prev_state.velocity,
                time_position=prev_state.time_position + 0.5
            )
            new_melody.append(new_note)
        
        new_melody.extend(melody[to_idx:])
        
        return new_melody
    
    def _optimize_rhythm_patterns(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """优化节奏模式，使其更流畅"""
        
        for i in range(1, len(melody)):
            curr = melody[i]
            prev = melody[i-1]
            
            # 避免连续的短音符或长音符
            if curr.duration == prev.duration:
                # 添加一些变化
                variation = random.choice([0.8, 1.2, 1.5])
                curr.duration = curr.duration * variation
                curr.duration = max(0.25, min(4.0, curr.duration))  # 限制在合理范围内
            
            # 确保节奏有韵律感
            if i > 1:
                prev_prev = melody[i-2]
                if curr.duration == prev.duration == prev_prev.duration:
                    # 打破连续重复
                    curr.duration = random.choice([0.5, 1.0, 2.0])
        
        return melody
    
    def _apply_emotion_consistency(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """根据情感类型应用一致性优化"""
        
        # 确定情感类型（这里简化处理，可以从状态或其他地方获取）
        emotion = self._detect_emotion(melody)
        
        if emotion == EmotionType.HAPPY:
            # 快乐音乐：增加上升音程
            melody = self._enhance_positive_intervals(melody)
        elif emotion == EmotionType.SAD:
            # 悲伤音乐：强调下降音程
            melody = self._enhance_negative_intervals(melody)
        elif emotion == EmotionType.MYSTERIOUS:
            # 神秘音乐：增加不协和音程
            melody = self._enhance_mysterious_intervals(melody)
        
        return melody
    
    def _detect_emotion(self, melody: List[OptimizedMelodyState]) -> EmotionType:
        """简单检测旋律情感（简化版）"""
        # 这里实现一个简单的情感检测算法
        # 在实际应用中，可以更复杂
        
        # 计算平均音程
        intervals = []
        for i in range(1, len(melody)):
            interval = melody[i].note.value - melody[i-1].note.value
            intervals.append(interval)
        
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        
        # 基于音程特征判断情感
        if avg_interval > 1:
            return EmotionType.HAPPY
        elif avg_interval < -1:
            return EmotionType.SAD
        else:
            return EmotionType.NEUTRAL
    
    def _enhance_positive_intervals(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """增强正向音程（快乐音乐）"""
        for i in range(1, len(melody)):
            curr = melody[i]
            prev = melody[i-1]
            
            # 如果是下降音程，可能改为上升
            if curr.note.value < prev.note.value and random.random() < 0.3:
                # 找到音阶内的上升替代
                scale_notes = [note.value for note in self.scale.notes]
                higher_notes = [n for n in scale_notes if n > prev.note.value]
                if higher_notes:
                    curr.note = NoteName(min(higher_notes, key=lambda x: abs(x - curr.note.value)))
        
        return melody
    
    def _enhance_negative_intervals(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """增强负向音程（悲伤音乐）"""
        for i in range(1, len(melody)):
            curr = melody[i]
            prev = melody[i-1]
            
            # 如果是上升音程，可能改为下降
            if curr.note.value > prev.note.value and random.random() < 0.3:
                # 找到音阶内的下降替代
                scale_notes = [note.value for note in self.scale.notes]
                lower_notes = [n for n in scale_notes if n < prev.note.value]
                if lower_notes:
                    curr.note = NoteName(max(lower_notes, key=lambda x: abs(x - curr.note.value)))
        
        return melody
    
    def _enhance_mysterious_intervals(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """增强神秘感音程"""
        for i in range(1, len(melody)):
            curr = melody[i]
            prev = melody[i-1]
            
            # 随机增加一些小的不协和
            if random.random() < 0.2:
                scale_notes = [note.value for note in self.scale.notes]
                dissonant = min(scale_notes, key=lambda x: abs(x - (prev.note.value + random.choice([-2, -1, 1, 2]))))
                curr.note = NoteName(dissonant)
        
        return melody
    
    def _enhance_climax(self, melody: List[OptimizedMelodyState]) -> List[OptimizedMelodyState]:
        """增强高潮部分"""
        if len(melody) < 8:
            return melody
        
        # 找到高潮位置（通常在2/3处）
        climax_pos = int(len(melody) * 0.67)
        
        # 确保高潮是最高音
        climax_note = melody[climax_pos]
        max_note = max(melody, key=lambda x: x.note.value)
        
        if climax_note.note.value < max_note.note.value:
            # 提高高潮音符
            scale_high_notes = [note for note in self.scale.notes if note.value > climax_note.note.value]
            if scale_high_notes:
                climax_note.note = max(scale_high_notes, key=lambda x: x.value)
                # 增加强度
                climax_note.velocity = min(127, climax_note.velocity + 20)
        
        # 高潮前后渐强渐弱
        for i in range(max(0, climax_pos - 3), climax_pos):
            melody[i].velocity = min(127, melody[i].velocity + 10)
        
        for i in range(climax_pos + 1, min(len(melody), climax_pos + 4)):
            melody[i].velocity = max(40, melody[i].velocity - 10)
        
        return melody


class HarmonyOptimizer:
    """和声优化器 - 优化旋律与伴奏的和声关系"""
    
    def __init__(self, scale: Scale):
        self.scale = scale
    
    def check_harmony(self, melody: List[OptimizedMelodyState], chord_progression: List[int]) -> Dict[str, int]:
        """检查旋律与和弦的和谐程度"""
        
        harmony_scores = {
            'consonance': 0,    # 协和度
            'tension': 0,       # 紧张度
            'resolution': 0     # 解决度
        }
        
        # 简化的和弦和谐度检查
        for i, note_state in enumerate(melody):
            chord_index = i % len(chord_progression)
            chord_tone = chord_progression[chord_index]
            note = note_state.note.value
            
            # 计算音程与和弦的关系
            interval = abs(note - chord_tone)
            interval_class = interval % 12
            
            # 基本音程协和度
            if interval_class in [0, 4, 7]:  # 完全协和
                harmony_scores['consonance'] += 3
            elif interval_class in [3, 6, 9]:  # 中等协和
                harmony_scores['consonance'] += 2
            elif interval_class in [1, 2, 5, 8, 10, 11]:  # 不协和
                harmony_scores['tension'] += 1
                if interval_class == [5, 8]:  # 有解决倾向
                    harmony_scores['resolution'] += 1
        
        return harmony_scores
    
    def optimize_for_harmony(self, melody: List[OptimizedMelodyState], chord_progression: List[int]) -> List[OptimizedMelodyState]:
        """根据和弦进行优化旋律"""
        scale_notes = [note.value for note in self.scale.notes]
        
        for i, note_state in enumerate(melody):
            chord_index = i % len(chord_progression)
            chord_tone = chord_progression[chord_index]
            current_note = note_state.note.value
            
            # 如果当前音符与和弦不和谐，调整到和谐的音符
            if current_note not in [chord_tone, chord_tone + 4, chord_tone + 7]:
                # 找到音阶内与和弦最和谐的音符
                best_note = min(scale_notes, key=lambda x: min(
                    abs(x - chord_tone), 
                    abs(x - (chord_tone + 4)), 
                    abs(x - (chord_tone + 7))
                ))
                note_state.note = NoteName(best_note)
        
        return melody