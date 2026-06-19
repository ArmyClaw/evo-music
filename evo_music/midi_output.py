"""
MIDI输出模块 - 使用MIDIUtil生成.mid文件
"""

from typing import List, Dict, Any, Optional, Union
import os
from dataclasses import dataclass

from .notes import NoteName
from .chords import Chord, ChordFactory
from .scales import Scale, ScaleFactory
from .music_theory import music_theory

try:
    from midiutil import MIDIFile
    MIDIUTIL_AVAILABLE = True
except ImportError:
    MIDIUTIL_AVAILABLE = False


@dataclass
class MIDIConfig:
    """MIDI配置"""
    tempo: int = 120
    time_signature: tuple = (4, 4)
    instrument: int = 0  # 0 = 钢琴
    channel: int = 0
    volume: float = 1.0


class MIDIGenerator:
    """MIDI生成器"""

    def __init__(self, config: Optional[MIDIConfig] = None):
        if not MIDIUTIL_AVAILABLE:
            raise ImportError("MIDIUtil未安装,请运行: pip install MIDIUtil")

        self.config = config or MIDIConfig()
        self.midi_file = MIDIFile(1)  # 单轨MIDI文件
        self.current_time = 0.0

        # 设置基本信息
        self.midi_file.addTempo(self.config.channel, 0, self.config.tempo)

    def _add_note(self, pitch: int, duration: float, volume: float = None):
        """添加音符到MIDI文件"""
        if volume is None:
            volume = self.config.volume

        # 将0.0-1.0的volume转换为0-127的MIDI力度值
        midi_volume = int(float(volume) * 127)
        
        self.midi_file.addNote(
            self.config.channel,
            self.config.instrument,
            pitch,
            int(self.current_time),
            float(duration),
            midi_volume
        )

    def _note_to_pitch(self, note: Union[str, NoteName]) -> int:
        """将音符转换为MIDI音高值"""
        if isinstance(note, str):
            note_obj = NoteName.from_string(note)
        else:
            note_obj = note

        # MIDI音高:C4 = 60, 每个半音增加1
        base_pitch = 60  # C4
        semitones = note_obj.value
        return base_pitch + semitones

    def _chord_to_pitches(self, chord: Chord) -> List[int]:
        """将和弦转换为音高值列表"""
        pitches = []
        for note in chord.notes:
            pitches.append(self._note_to_pitch(note))
        return pitches

    def add_chord(self, chord: Chord, duration: float = 4.0, volume: float = None):
        """添加和弦到MIDI文件"""
        if volume is None:
            volume = self.config.volume

        pitches = self._chord_to_pitches(chord)
        for i, pitch in enumerate(pitches):
            # 稍微错开每个音符的开始时间,避免完全重叠
            start_time = int(self.current_time + i * 0.1)
            self.midi_file.addNote(
                self.config.channel,
                self.config.instrument,
                pitch,
                start_time,
                float(duration),
                float(volume)
            )

    def add_scale(self, scale: Scale, duration: float = 1.0, ascending: bool = True):
        """添加音阶到MIDI文件"""
        notes = scale.notes if ascending else scale.notes[::-1]

        for note in notes:
            pitch = self._note_to_pitch(note)
            self._add_note(pitch, duration)
            self.current_time += duration

    def add_rhythm_pattern(self, pattern_name: str, chord: Chord, measures: int = 4):
        """添加节奏模式"""
        # 这里可以根据不同的节奏模式添加相应的音符
        # 简化版:每小节播放和弦的根音
        beat_duration = 1.0  # 4分音符
        for _ in range(measures * 4):  # 4拍/小节 * 小节数
            root_pitch = self._note_to_pitch(chord.root_note)
            self._add_note(root_pitch, beat_duration)
            self.current_time += beat_duration

    def add_chord_progression(self, progression: List[Chord], measure_per_chord: int = 1):
        """添加和弦进行"""
        beat_duration = 1.0  # 4分音符
        beats_per_chord = measure_per_chord * 4  # 每个和弦占用的拍数

        for chord in progression:
            # 添加和弦的所有音符
            pitches = self._chord_to_pitches(chord)
            for pitch in pitches:
                self._add_note(pitch, beat_duration * beats_per_chord)

            self.current_time += beat_duration * beats_per_chord

    def add_melody(self, notes: List[Union[str, NoteName]], durations: List[float]):
        """添加旋律"""
        if len(notes) != len(durations):
            raise ValueError("音符数量和持续时间数量不匹配")

        for note, duration in zip(notes, durations):
            if isinstance(note, str):
                note_obj = NoteName.from_string(note)
            else:
                note_obj = note

            pitch = self._note_to_pitch(note_obj)
            self._add_note(pitch, duration)
            self.current_time += duration

    def add_arpeggio(self, chord: Chord, pattern: str = "up", repeats: int = 1):
        """添加琶音"""
        if pattern == "up":
            notes = chord.notes
        elif pattern == "down":
            notes = chord.notes[::-1]
        elif pattern == "up_down":
            notes = chord.notes[:-1] + chord.notes[::-1]
        else:
            notes = chord.notes

        beat_duration = 0.5  # 8分音符

        for _ in range(repeats):
            for note in notes:
                pitch = self._note_to_pitch(note)
                self._add_note(pitch, beat_duration)
                self.current_time += beat_duration

    def generate_progression_demo(self, root_note: str = "C", scale_type: str = "major",
                                 style: str = "classic_pop", length: int = 4):
        """生成和弦进行演示"""
        # 生成和弦进行
        progression = music_theory.generate_chord_progression(
            root_note, scale_type, style, length
        )

        # 添加和弦进行
        self.add_chord_progression(progression)

        return progression

    def save(self, filename: str):
        """保存MIDI文件"""
        # 确保文件名以.mid结尾
        if not filename.endswith('.mid'):
            filename += '.mid'

        # 确保目录存在
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)

        with open(filename, 'wb') as f:
            self.midi_file.writeFile(f)

        return filename


class MIDIExporter:
    """MIDI导出器"""

    def __init__(self, config: Optional[MIDIConfig] = None):
        self.config = config or MIDIConfig()
        self.generator = MIDIGenerator(config)

    def export_scale(self, root_note: str, scale_type: str = "major",
                    filename: Optional[str] = None) -> str:
        """导出音阶为MIDI文件"""
        scale = ScaleFactory.create_scale(NoteName.from_string(root_note), scale_type)

        if filename is None:
            filename = f"{root_note}_{scale_type}_scale.mid"

        self.generator.add_scale(scale)
        return self.generator.save(filename)

    def export_chord(self, root_note: str, chord_type: str = "major",
                    filename: Optional[str] = None) -> str:
        """导出和弦为MIDI文件"""
        chord = ChordFactory.create_chord(NoteName.from_string(root_note), chord_type)

        if filename is None:
            filename = f"{root_note}_{chord_type}_chord.mid"

        self.generator.add_chord(chord)
        return self.generator.save(filename)

    def export_progression(self, root_note: str, scale_type: str = "major",
                         style: str = "classic_pop", length: int = 4,
                         filename: Optional[str] = None) -> str:
        """导出和弦进行为MIDI文件"""
        progression = music_theory.generate_chord_progression(
            root_note, scale_type, style, length
        )
        
        if filename is None:
            filename = f"{root_note}_{scale_type}_{style}_progression.mid"
        
        self.generator.add_chord_progression(progression)
        return self.generator.save(filename)
    
    def export_chord_progression(self, root_note: str, scale_type: str = "major",
                                style: str = "classic_pop", length: int = 4,
                                filename: Optional[str] = None) -> str:
        """导出和弦进行为MIDI文件（向后兼容）"""
        return self.export_progression(root_note, scale_type, style, length, filename)

    def export_music_demo(self, root_note: str = "C", scale_type: str = "major",
                          style: str = "classic_pop", filename: Optional[str] = None) -> str:
        """导出音乐演示文件"""
        if filename is None:
            filename = f"{root_note}_{scale_type}_{style}_demo.mid"

        # 生成和弦进行演示
        progression = self.generator.generate_progression_demo(root_note, scale_type, style)

        # 添加一些装饰性的琶音
        for chord in progression:
            self.generator.add_arpeggio(chord, "up", 2)
            self.generator.current_time += 1.0  # 间隔

        return self.generator.save(filename)

    def export_random_progression(self, root_note: str = "C", scale_type: str = "major",
                                 length: int = 4, filename: Optional[str] = None) -> str:
        """导出随机和弦进行"""
        progression = music_theory.get_random_chord_progression(root_note, scale_type, length)

        if filename is None:
            filename = f"{root_note}_{scale_type}_random_progression.mid"

        self.generator.add_chord_progression(progression)
        return self.generator.save(filename)


# ============ 快捷函数 ============

def export_scale_midi(root_note: str, scale_type: str = "major",
                     filename: Optional[str] = None) -> str:
    """快捷函数:导出音阶为MIDI"""
    exporter = MIDIExporter()
    return exporter.export_scale(root_note, scale_type, filename)

def export_chord_midi(root_note: str, chord_type: str = "major",
                     filename: Optional[str] = None) -> str:
    """快捷函数:导出和弦为MIDI"""
    exporter = MIDIExporter()
    return exporter.export_chord(root_note, chord_type, filename)

def export_progression_midi(root_note: str, scale_type: str = "major",
                           style: str = "classic_pop", length: int = 4,
                           filename: Optional[str] = None) -> str:
    """快捷函数:导出和弦进行为MIDI"""
    exporter = MIDIExporter()
    return exporter.export_chord_progression(root_note, scale_type, style, length, filename)

def export_music_demo_midi(root_note: str = "C", scale_type: str = "major",
                          style: str = "classic_pop", filename: Optional[str] = None) -> str:
    """快捷函数:导出音乐演示为MIDI"""
    exporter = MIDIExporter()
    return exporter.export_music_demo(root_note, scale_type, style, filename)


# ============ 示例和演示功能 ============

def demonstrate_midi_output():
    """演示MIDI输出功能"""
    print("=== MIDI输出功能演示 ===")

    if not MIDIUTIL_AVAILABLE:
        print("错误:MIDIUtil未安装,无法演示")
        return

    try:
        # 创建导出器
        exporter = MIDIExporter()

        # 简化演示:只生成一个和弦进行
        print("\n1. 生成和弦进行演示...")
        demo_file = exporter.export_progression("C", "major", "classic_pop", 4)
        print(f"已生成: {demo_file}")

        # 导出音阶
        print("\n2. 导出音阶...")
        scale_file = exporter.export_scale("C", "major")
        print(f"已生成: {scale_file}")

        print("\n=== MIDI文件已生成完成 ===")

    except Exception as e:
        print(f"生成MIDI文件时出错: {e}")
        # 使用简单的演示作为后备
        print("使用简单演示...")
        try:
            import simple_demo
            simple_demo.simple_midi_demo()
        except:
            print("无法生成演示文件")


if __name__ == "__main__":
    demonstrate_midi_output()