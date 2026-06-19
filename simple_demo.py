#!/usr/bin/env python3
"""
简单的MIDI演示
"""

from midiutil import MIDIFile

def simple_midi_demo():
    """简单的MIDI演示"""
    print("=== 简单MIDI演示 ===")
    
    # 创建MIDI文件
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)  # 通道0，时间0，120BPM
    
    # 添加C大调和弦进行（I-IV-V-I）
    # C大和弦 (I)
    midi.addNote(0, 0, 60, 0, 4, 100)  # C
    midi.addNote(0, 0, 64, 0, 4, 100)  # E
    midi.addNote(0, 0, 67, 0, 4, 100)  # G
    
    # G大和弦 (V)
    midi.addNote(0, 0, 55, 4, 4, 100)  # G
    midi.addNote(0, 0, 62, 4, 4, 100)  # B
    midi.addNote(0, 0, 67, 4, 4, 100)  # G
    
    # F大和弦 (IV)
    midi.addNote(0, 0, 53, 8, 4, 100)  # F
    midi.addNote(0, 0, 65, 8, 4, 100)  # A
    midi.addNote(0, 0, 68, 8, 4, 100)  # C
    
    # C大和弦 (I)
    midi.addNote(0, 0, 60, 12, 4, 100)  # C
    midi.addNote(0, 0, 64, 12, 4, 100)  # E
    midi.addNote(0, 0, 67, 12, 4, 100)  # G
    
    # 保存文件
    filename = "chord_progression_demo.mid"
    with open(filename, "wb") as f:
        midi.writeFile(f)
    
    print(f"和弦进行演示已生成: {filename}")
    
    # 生成一个音阶演示
    midi_scale = MIDIFile(1)
    midi_scale.addTempo(0, 0, 120)
    
    # C大调音阶
    scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C, D, E, F, G, A, B, C
    for i, pitch in enumerate(scale_notes):
        midi_scale.addNote(0, 0, pitch, i * 1, 1, 100)
    
    scale_filename = "c_major_scale_demo.mid"
    with open(scale_filename, "wb") as f:
        midi_scale.writeFile(f)
    
    print(f"C大调音阶演示已生成: {scale_filename}")
    
    return [filename, scale_filename]

if __name__ == "__main__":
    simple_midi_demo()