"""
适应度函数模块
实现旋律的多种评分标准：
- 音程平滑度：旋律跳跃的合理性
- 节奏规律性：时值分布的规律性
- 调性一致性：与指定调音阶的一致性
"""

from typing import List, Dict, Tuple
import math
from dataclasses import dataclass
from .notes import NoteName
from .scales import Scale
from .melody_optimizer import OptimizedMelodyState


@dataclass
class FitnessScore:
    """适应度评分结果"""
    total_score: float                    # 总体适应度分数 (0-100)
    interval_smoothness: float            # 音程平滑度分数 (0-100)
    rhythm_regularity: float              # 节奏规律性分数 (0-100)
    tonal_consistency: float              # 调性一致性分数 (0-100)
    detailed_metrics: Dict[str, float]   # 详细指标


class MelodyFitnessEvaluator:
    """旋律适应度评估器"""
    
    def __init__(self, scale: Scale):
        self.scale = scale
        self.scale_notes_values = [note.value for note in self.scale.notes]
        self.preferred_intervals = [0, 1, 2, 3, 4, 5, 7, 8, 9]  # 优选音程（半音）
        self.max_acceptable_interval = 12  # 最大可接受音程（半音）
        
    def evaluate_fitness(self, melody: List[OptimizedMelodyState]) -> FitnessScore:
        """评估旋律适应度"""
        
        # 计算各项评分
        interval_smoothness = self._evaluate_interval_smoothness(melody)
        rhythm_regularity = self._evaluate_rhythm_regularity(melody)
        tonal_consistency = self._evaluate_tonal_consistency(melody)
        
        # 计算总体评分（加权平均）
        weights = {
            'interval_smoothness': 0.4,    # 音程平滑度权重 40%
            'rhythm_regularity': 0.3,      # 节奏规律性权重 30%
            'tonal_consistency': 0.3       # 调性一致性权重 30%
        }
        
        total_score = (
            interval_smoothness * weights['interval_smoothness'] +
            rhythm_regularity * weights['rhythm_regularity'] +
            tonal_consistency * weights['tonal_consistency']
        )
        
        # 获取详细指标
        detailed_metrics = self._get_detailed_metrics(melody)
        
        return FitnessScore(
            total_score=total_score,
            interval_smoothness=interval_smoothness,
            rhythm_regularity=rhythm_regularity,
            tonal_consistency=tonal_consistency,
            detailed_metrics=detailed_metrics
        )
    
    def _evaluate_interval_smoothness(self, melody: List[OptimizedMelodyState]) -> float:
        """评估音程平滑度 (0-100分)"""
        if len(melody) < 2:
            return 100.0
        
        smoothness_score = 0.0
        total_intervals = 0
        
        for i in range(1, len(melody)):
            prev_note = melody[i-1].note.value
            curr_note = melody[i].note.value
            octave_diff = melody[i].octave - melody[i-1].octave
            interval = abs(curr_note - prev_note) + octave_diff * 12
            
            # 计算平滑度分数
            if interval == 0:  # 同音
                score = 100.0
            elif interval <= 3:  # 小音程
                score = 95.0
            elif interval <= 5:  # 中等音程
                score = 80.0
            elif interval <= 7:  # 大音程
                score = 65.0
            elif interval <= 10:  # 很大音程
                score = 40.0
            elif interval <= self.max_acceptable_interval:  # 极大音程
                score = 20.0
            else:  # 不可接受的音程
                score = 0.0
            
            smoothness_score += score
            total_intervals += 1
        
        return smoothness_score / total_intervals if total_intervals > 0 else 100.0
    
    def _evaluate_rhythm_regularity(self, melody: List[OptimizedMelodyState]) -> float:
        """评估节奏规律性 (0-100分)"""
        if len(melody) < 3:
            return 100.0
        
        # 分析时值分布
        durations = [state.duration for state in melody]
        
        # 计算时值变化率
        variation_score = 0.0
        for i in range(1, len(durations)):
            variation = abs(durations[i] - durations[i-1])
            variation_score += 100 - min(100, variation * 10)  # 变化越小分数越高
        
        duration_diversity_score = 0.0
        unique_durations = set(durations)
        
        # 适度的时值多样性（太单调或太多样都不好）
        if len(unique_durations) == 1:
            duration_diversity_score = 50.0  # 太单调
        elif len(unique_durations) <= 3:
            duration_diversity_score = 85.0  # 适度多样
        elif len(unique_durations) <= 5:
            duration_diversity_score = 75.0  # 比较多样
        else:
            duration_diversity_score = 60.0  # 太多样
        
        # 计算节奏模式规律性
        pattern_score = self._evaluate_rhythm_patterns(melody)
        
        # 综合评分
        total_score = (variation_score / len(durations) * 0.4 + 
                      duration_diversity_score * 0.3 + 
                      pattern_score * 0.3)
        
        return total_score
    
    def _evaluate_rhythm_patterns(self, melody: List[OptimizedMelodyState]) -> float:
        """评估节奏模式规律性"""
        if len(melody) < 4:
            return 100.0
        
        # 分析节奏模式的重复性
        durations = [state.duration for state in melody]
        pattern_length = min(4, len(durations) // 2)
        
        # 查找重复模式
        pattern_scores = []
        for start in range(len(durations) - pattern_length):
            pattern = durations[start:start + pattern_length]
            repeats = 0
            
            for check_start in range(start + 1, len(durations) - pattern_length + 1):
                check_pattern = durations[check_start:check_start + pattern_length]
                if pattern == check_pattern:
                    repeats += 1
            
            pattern_scores.append(repeats)
        
        # 模式重复越多，节奏越规律
        avg_repeats = sum(pattern_scores) / len(pattern_scores) if pattern_scores else 0
        return min(100, avg_repeats * 25 + 50)
    
    def _evaluate_tonal_consistency(self, melody: List[OptimizedMelodyState]) -> float:
        """评估调性一致性 (0-100分)"""
        if len(melody) == 0:
            return 0.0
        
        # 统计音符在音阶中的分布
        in_scale_count = 0
        total_notes = 0
        
        for state in melody:
            note_value = state.note.value
            if note_value in self.scale_notes_values:
                in_scale_count += 1
            total_notes += 1
        
        # 基础音阶一致性分数
        scale_consistency = (in_scale_count / total_notes) * 100 if total_notes > 0 else 0.0
        
        # 音符分布合理性（避免过度集中在某些音）
        note_distribution = {}
        for state in melody:
            note_key = state.note.value
            note_distribution[note_key] = note_distribution.get(note_key, 0) + 1
        
        distribution_score = self._evaluate_note_distribution(note_distribution)
        
        # 综合评分
        return scale_consistency * 0.7 + distribution_score * 0.3
    
    def _evaluate_note_distribution(self, note_distribution: Dict[int, int]) -> float:
        """评估音符分布的合理性"""
        if not note_distribution:
            return 0.0
        
        total_notes = sum(note_distribution.values())
        unique_notes = len(note_distribution)
        
        # 计算分布均衡性
        max_count = max(note_distribution.values())
        min_count = min(note_distribution.values())
        
        # 分布越均衡，分数越高
        balance_ratio = (total_notes / unique_notes - min_count) / (max_count - min_count) if max_count != min_count else 1.0
        distribution_balance = balance_ratio * 50 + 50  # 50-100分
        
        # 音符使用多样性（太少或太多都不好）
        if unique_notes == 1:
            diversity_score = 30.0  # 单调
        elif unique_notes <= 3:
            diversity_score = 70.0  # 适中
        elif unique_notes <= 6:
            diversity_score = 90.0  # 良好
        else:
            diversity_score = 75.0  # 稍多
        
        return (distribution_balance * 0.6 + diversity_score * 0.4)
    
    def _get_detailed_metrics(self, melody: List[OptimizedMelodyState]) -> Dict[str, float]:
        """获取详细评分指标"""
        if len(melody) == 0:
            return {}
        
        metrics = {}
        
        # 音程统计
        intervals = []
        for i in range(1, len(melody)):
            prev_note = melody[i-1].note.value
            curr_note = melody[i].note.value
            octave_diff = melody[i].octave - melody[i-1].octave
            interval = abs(curr_note - prev_note) + octave_diff * 12
            intervals.append(interval)
        
        if intervals:
            metrics['avg_interval'] = sum(intervals) / len(intervals)
            metrics['max_interval'] = max(intervals)
            metrics['min_interval'] = min(intervals)
            
            # 音程分布统计
            small_intervals = sum(1 for i in intervals if i <= 3)
            medium_intervals = sum(1 for i in intervals if 4 <= i <= 7)
            large_intervals = sum(1 for i in intervals if i > 7)
            
            metrics['small_interval_ratio'] = small_intervals / len(intervals)
            metrics['medium_interval_ratio'] = medium_intervals / len(intervals)
            metrics['large_interval_ratio'] = large_intervals / len(intervals)
        
        # 时值统计
        durations = [state.duration for state in melody]
        metrics['avg_duration'] = sum(durations) / len(durations) if durations else 0
        metrics['duration_variance'] = sum((d - metrics['avg_duration'])**2 for d in durations) / len(durations) if durations else 0
        
        # 音阶覆盖
        in_scale_notes = sum(1 for state in melody if state.note.value in self.scale_notes_values)
        metrics['scale_coverage'] = in_scale_notes / len(melody) if melody else 0
        
        # 音符种类
        unique_notes = len(set(state.note.value for state in melody))
        metrics['unique_note_count'] = unique_notes
        metrics['unique_note_ratio'] = unique_notes / len(melody) if melody else 0
        
        return metrics
    
    def compare_melodies(self, melody1: List[OptimizedMelodyState], 
                        melody2: List[OptimizedMelodyState]) -> Dict[str, any]:
        """比较两个旋律的适应度"""
        score1 = self.evaluate_fitness(melody1)
        score2 = self.evaluate_fitness(melody2)
        
        comparison = {
            'melody1': {
                'total_score': score1.total_score,
                'interval_smoothness': score1.interval_smoothness,
                'rhythm_regularity': score1.rhythm_regularity,
                'tonal_consistency': score1.tonal_consistency
            },
            'melody2': {
                'total_score': score2.total_score,
                'interval_smoothness': score2.interval_smoothness,
                'rhythm_regularity': score2.rhythm_regularity,
                'tonal_consistency': score2.tonal_consistency
            },
            'better_melody': 1 if score1.total_score > score2.total_score else 2,
            'score_difference': abs(score1.total_score - score2.total_score)
        }
        
        return comparison