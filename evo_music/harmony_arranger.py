"""
和声编排器 - 根据旋律自动生成和声层
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import random

from .notes import NoteName
from .chords import Chord, ChordFactory, ChordType, ChordProgressionAnalyzer
from .scales import Scale, ScaleType, ScaleFactory
from .melody import MelodyConfig, EmotionType
from .music_theory import MusicTheory


class HarmonyStyle(Enum):
    """和声风格"""
    SIMPLE = "simple"          # 简单四部和声
    POP = "pop"               # 流行和声
    JAZZ = "jazz"             # 爵士和声
    CLASSICAL = "classical"   # 古典和声
    MODERN = "modern"         # 现代和声
    CHINESE = "chinese"       # 中国风和声


@dataclass
class HarmonyConfig:
    """和声编排配置"""
    style: HarmonyStyle = HarmonyStyle.POP
    chord_density: float = 0.3  # 和弦密度（每小节的和弦数）
    voice_leading: bool = True  # 声部进行
    use_inversions: bool = True  # 使用转位
    extensions_level: int = 1    # 扩展音级别（0-3）
    bass_walk: bool = False      # 低音行走
    pad_voices: int = 2         # 垫底声部数量
    
    @classmethod
    def get_default_for_emotion(cls, emotion: EmotionType) -> 'HarmonyConfig':
        """根据情感获取默认配置"""
        configs = {
            EmotionType.HAPPY: cls(HarmonyStyle.POP, chord_density=0.4, extensions_level=1),
            EmotionType.SAD: cls(HarmonyStyle.CLASSICAL, chord_density=0.2, extensions_level=2),
            EmotionType.MYSTERIOUS: cls(HarmonyStyle.JAZZ, chord_density=0.3, extensions_level=2),
            EmotionType.EPIC: cls(HarmonyStyle.MODERN, chord_density=0.5, extensions_level=3),
            EmotionType.PEACEFUL: cls(HarmonyStyle.SIMPLE, chord_density=0.25, extensions_level=0),
            EmotionType.DARK: cls(HarmonyStyle.JAZZ, chord_density=0.3, extensions_level=2),
            EmotionType.BRIGHT: cls(HarmonyStyle.POP, chord_density=0.4, extensions_level=1),
            EmotionType.CHINESE: cls(HarmonyStyle.CHINESE, chord_density=0.3, extensions_level=1),
            EmotionType.BLUES: cls(HarmonyStyle.JAZZ, chord_density=0.4, extensions_level=2),
            EmotionType.NEUTRAL: cls(HarmonyStyle.POP, chord_density=0.3, extensions_level=1),
        }
        return configs.get(emotion, cls())


class HarmonyArranger:
    """和声编排器主类"""
    
    def __init__(self, config: HarmonyConfig):
        self.config = config
        self.chord_factory = ChordFactory()
        self.scale_factory = ScaleFactory()
        self.music_theory = MusicTheory()
        
    def arrange_harmony_for_melody(self, melody_notes: List[Tuple[int, int]], 
                                   scale: Scale, time_signature: Tuple[int, int] = (4, 4)) -> Dict[str, Any]:
        """
        为旋律编排和声
        
        Args:
            melody_notes: 旋律音符列表，每个元素为 (音符值, 时值)
            scale: 调式
            time_signature: 拍号
        
        Returns:
            包含和声编排结果的字典
        """
        # 分析旋律特征
        melody_analysis = self._analyze_melody(melody_notes, scale)
        
        # 生成基础和弦进行
        chord_progression = self._generate_chord_progression(melody_analysis, scale)
        
        # 将和弦分配到小节
        chord_distribution = self._distribute_chords_to_measures(chord_progression, time_signature, melody_notes)
        
        # 生成各个声部的音符
        harmony_voices = self._generate_harmony_voices(chord_distribution, melody_analysis, scale)
        
        return {
            "chord_progression": chord_distribution,
            "harmony_voices": harmony_voices,
            "melody_analysis": melody_analysis,
            "config": self.config
        }
    
    def _analyze_melody(self, melody_notes: List[Tuple[int, int]], scale: Scale) -> Dict[str, Any]:
        """分析旋律特征"""
        # 音域分析
        note_values = [note[0] for note in melody_notes]
        pitch_range = max(note_values) - min(note_values)
        
        # 关键音检测（强拍、长音、高音）
        strong_beats = []
        long_notes = []
        climax_notes = []
        
        total_duration = sum(note[1] for note in melody_notes)
        
        for i, (note_value, duration) in enumerate(melody_notes):
            # 检查是否在强拍上（假设4/4拍，第1、3拍为强拍）
            beat_position = i % 4
            if beat_position in [0, 2]:  # 第1、3拍
                strong_beats.append(i)
            
            # 长音（超过1拍）
            if duration > 1:
                long_notes.append(i)
            
            # 高音（音域最高的20%）
            if note_value >= max(note_values) - pitch_range * 0.2:
                climax_notes.append(i)
        
        # 调性分析
        scale_degrees = self._get_scale_degrees(note_values, scale)
        
        return {
            "pitch_range": pitch_range,
            "strong_beats": strong_beats,
            "long_notes": long_notes,
            "climax_notes": climax_notes,
            "total_duration": total_duration,
            "scale_degrees": scale_degrees,
            "note_count": len(melody_notes),
            "average_duration": total_duration / len(melody_notes)
        }
    
    def _generate_chord_progression(self, melody_analysis: Dict[str, Any], scale: Scale) -> List[Chord]:
        """生成和弦进行"""
        chords = []
        
        # 基于调性生成基本和弦
        scale_chords = self._generate_scale_chords(scale)
        
        # 根据情感和风格选择和弦进行
        if self.config.style == HarmonyStyle.POP:
            progression = self._generate_pop_progression(scale_chords, melody_analysis)
        elif self.config.style == HarmonyStyle.JAZZ:
            progression = self._generate_jazz_progression(scale_chords, melody_analysis)
        elif self.config.style == HarmonyStyle.CLASSICAL:
            progression = self._generate_classical_progression(scale_chords, melody_analysis)
        elif self.config.style == HarmonyStyle.MODERN:
            progression = self._generate_modern_progression(scale_chords, melody_analysis)
        elif self.config.style == HarmonyStyle.CHINESE:
            progression = self._generate_chinese_progression(scale_chords, melody_analysis)
        else:
            progression = self._generate_simple_progression(scale_chords, melody_analysis)
        
        return progression
    
    def _generate_pop_progression(self, scale_chords: List[Chord], melody_analysis: Dict[str, Any]) -> List[Chord]:
        """生成流行音乐和弦进行"""
        # 经典流行进行：I-V-vi-IV
        if len(scale_chords) >= 4:
            return [
                scale_chords[0],  # I
                scale_chords[4],  # V
                scale_chords[2],  # vi
                scale_chords[3],  # IV
            ]
        
        # 简化版本
        return scale_chords[:4]
    
    def _generate_jazz_progression(self, scale_chords: List[Chord], melody_analysis: Dict[str, Any]) -> List[Chord]:
        """生成爵士和弦进行"""
        # 爵士标准进行：ii-V-I
        if len(scale_chords) >= 3:
            return [
                scale_chords[1],  # ii
                scale_chords[4],  # V
                scale_chords[0],  # I
            ]
        
        # 使用七和弦
        seventh_chords = [self._add_seventh_extension(chord) for chord in scale_chords]
        return seventh_chords[:3]
    
    def _generate_classical_progression(self, scale_chords: List[Chord], melody_analysis: Dict[str, Any]) -> List[Chord]:
        """生成古典和弦进行"""
        # 经典古典进行：I-IV-V-I
        if len(scale_chords) >= 5:
            return [
                scale_chords[0],  # I
                scale_chords[3],  # IV
                scale_chords[4],  # V
                scale_chords[0],  # I
            ]
        
        return scale_chords[:4]
    
    def _generate_modern_progression(self, scale_chords: List[Chord], melody_analysis: Dict[str, Any]) -> List[Chord]:
        """生成现代和弦进行"""
        # 现代流行进行：vi-IV-I-V
        if len(scale_chords) >= 5:
            return [
                scale_chords[2],  # vi
                scale_chords[3],  # IV
                scale_chords[0],  # I
                scale_chords[4],  # V
            ]
        
        # 添加扩展音
        extended_chords = [self._add_extensions(chord, self.config.extensions_level) for chord in scale_chords]
        return extended_chords[:4]
    
    def _generate_chinese_progression(self, scale_chords: List[Chord], melody_analysis: Dict[str, Any]) -> List[Chord]:
        """生成中国风和弦进行"""
        # 中国风常用和弦进行
        if len(scale_chords) >= 5:
            return [
                scale_chords[0],  # I
                scale_chords[2],  # iii (模拟五声调式)
                scale_chords[4],  # V
                scale_chords[3],  # IV
            ]
        
        return scale_chords[:4]
    
    def _generate_simple_progression(self, scale_chords: List[Chord], melody_analysis: Dict[str, Any]) -> List[Chord]:
        """生成简单和弦进行"""
        return scale_chords[:3]
    
    def _generate_scale_chords(self, scale: Scale) -> List[Chord]:
        """根据调式生成和弦"""
        chords = []
        
        # 生成各级三和弦
        scale_notes = scale.get_notes()
        
        for i, scale_note in enumerate(scale_notes):
            if i < 7:  # 只生成前7级
                # 确定和弦类型
                chord_type = self._get_chord_type_for_degree(i)
                
                # 创建和弦
                chord = self.chord_factory.create_triad(scale_note, chord_type)
                
                chords.append(chord)
        
        return chords
    
    def _get_chord_type_for_degree(self, degree: int) -> str:
        """根据音级确定和弦类型"""
        # 大调：I-IV-V为大三，ii-iii-vi为小三，vii°为减
        if degree in [0, 3, 4]:  # I, IV, V
            return ChordType.MAJOR
        elif degree in [1, 2, 5]:  # ii, iii, vi
            return ChordType.MINOR
        else:  # vii°
            return ChordType.DIMINISHED
    
    def _add_seventh_extension(self, chord: Chord) -> Chord:
        """添加七度扩展"""
        chord.extensions.append(7)
        return chord
    
    def _add_extensions(self, chord: Chord, level: int) -> Chord:
        """添加扩展音"""
        if level >= 1:
            chord.extensions.append(7)
        if level >= 2:
            chord.extensions.append(9)
        if level >= 3:
            chord.extensions.append(11)
        
        return chord
    
    def _distribute_chords_to_measures(self, chord_progression: List[Chord], 
                                     time_signature: Tuple[int, int], 
                                     melody_notes: List[Tuple[int, int]]) -> List[Dict[str, Any]]:
        """将和弦分配到小节"""
        beats_per_measure = time_signature[0]
        chord_distribution = []
        
        # 计算总小节数
        total_duration = sum(note[1] for note in melody_notes)
        total_measures = max(1, int(total_duration / beats_per_measure))
        
        # 根据和弦密度决定每个小节使用什么和弦
        chords_per_measure = max(1, int(beats_per_measure * self.config.chord_density))
        
        for measure in range(total_measures):
            # 选择当前小节使用的和弦
            chord_index = (measure * chords_per_measure) % len(chord_progression)
            chord = chord_progression[chord_index]
            
            # 确定和弦开始位置
            start_beat = measure * beats_per_measure
            
            # 应用转位（如果启用）
            if self.config.use_inversions:
                chord = self._apply_inversion(chord, measure)
            
            chord_distribution.append({
                "measure": measure,
                "start_beat": start_beat,
                "chord": chord,
                "duration": beats_per_measure,
                "chord_index": chord_index
            })
        
        return chord_distribution
    
    def _apply_inversion(self, chord: Chord, measure: int) -> Chord:
        """应用和弦转位"""
        # 简单的转位逻辑：交替使用原位和第一转位
        inversion_type = measure % 3  # 0=原位，1=第一转位，2=第二转位
        
        if inversion_type == 1:
            # 第一转位：将根音移到上方
            chord.bass_note = chord.notes[0]
            chord.notes = chord.notes[1:] + [chord.notes[0]]
        elif inversion_type == 2:
            # 第二转位：将三音移到上方
            chord.bass_note = chord.notes[1]
            chord.notes = chord.notes[2:] + chord.notes[:2]
        
        return chord
    
    def _generate_harmony_voices(self, chord_distribution: List[Dict[str, Any]], 
                                melody_analysis: Dict[str, Any], 
                                scale: Scale) -> Dict[str, List[Tuple[int, int]]]:
        """生成和声声部的音符"""
        voices = {
            "harmony": [],      # 和声声部
            "bass": [],        # 低音声部
            "pad": []          # 垫底声部
        }
        
        for measure_info in chord_distribution:
            chord = measure_info["chord"]
            start_beat = measure_info["start_beat"]
            duration = measure_info["duration"]
            
            # 生成和声声部音符
            harmony_notes = self._generate_harmony_notes(chord, scale, start_beat, duration)
            voices["harmony"].extend(harmony_notes)
            
            # 生成低音声部音符
            bass_notes = self._generate_bass_notes(chord, start_beat, duration)
            voices["bass"].extend(bass_notes)
            
            # 生成垫底声部音符
            for i in range(self.config.pad_voices):
                pad_notes = self._generate_pad_notes(chord, scale, start_beat, duration, i)
                voices[f"pad_{i}"] = pad_notes
        
        return voices
    
    def _generate_harmony_notes(self, chord: Chord, scale: Scale, start_beat: int, duration: int) -> List[Tuple[int, int]]:
        """生成和声声部音符"""
        notes = []
        
        # 选择和弦中的3-4个音
        chord_notes_to_use = min(4, len(chord.notes))
        selected_notes = chord.notes[:chord_notes_to_use]
        
        # 在指定时值内分配音符
        beat_position = start_beat
        for i, note in enumerate(selected_notes):
            note_duration = duration // chord_notes_to_use
            note_value = note.value
            notes.append((note_value, note_duration))
            
            # 添加一些节奏变化
            if i < len(selected_notes) - 1:
                notes.append((note_value, 0.5))  # 短暂的保持音
        
        return notes
    
    def _generate_bass_notes(self, chord: Chord, start_beat: int, duration: int) -> List[Tuple[int, int]]:
        """生成低音声部音符"""
        notes = []
        
        # 低音使用根音
        bass_note = chord.bass_note if chord.bass_note else chord.root_note
        
        # 如果启用低音行走，添加一些变化
        if self.config.bass_walk:
            # 简单的行走：根音->五音->根音
            notes.extend([
                (bass_note.value, duration * 0.4),
                (bass_note.value + 7, duration * 0.4),  # 五度
                (bass_note.value, duration * 0.2)
            ])
        else:
            # 简单的根音保持
            notes.append((bass_note.value, duration))
        
        return notes
    
    def _generate_pad_notes(self, chord: Chord, scale: Scale, start_beat: int, duration: int, voice_index: int) -> List[Tuple[int, int]]:
        """生成垫底声部音符"""
        notes = []
        
        # 垫底声部使用较长的音符，音高在和声范围内
        chord_note = chord.notes[voice_index % len(chord.notes)]
        
        # 根据声部索引调整音高
        if voice_index == 0:
            # 第一个垫底声部：较高的和音
            adjusted_note = chord_note.value + 12  # 高八度
        else:
            # 第二个垫底声部：较低的和音
            adjusted_note = chord_note.value - 12  # 低八度
        
        notes.append((adjusted_note, duration))
        
        return notes
    
    def _get_scale_degrees(self, note_values: List[int], scale: Scale) -> List[int]:
        """获取音符在调式中的音级"""
        scale_degrees = []
        scale_notes = scale.get_notes()
        
        for note_value in note_values:
            # 找到最接近的调式音级
            closest_degree = 0
            min_distance = float('inf')
            
            for i, scale_note in enumerate(scale_notes):
                distance = abs(note_value - scale_note.value)
                if distance < min_distance:
                    min_distance = distance
                    closest_degree = i
            
            scale_degrees.append(closest_degree)
        
        return scale_degrees