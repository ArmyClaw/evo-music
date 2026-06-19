#!/usr/bin/env python3
"""
简单的MIDI测试脚本
"""

from midiutil import MIDIFile

# 创建简单的MIDI文件
midi = MIDIFile(1)
midi.addTempo(0, 0, 120)

# 添加音符
midi.addNote(0, 0, 60, 0, 4, 100)
midi.addNote(0, 0, 62, 4, 4, 100)
midi.addNote(0, 0, 64, 8, 4, 100)

# 保存文件
with open("simple_test.mid", "wb") as f:
    midi.writeFile(f)

print("简单MIDI文件已生成: simple_test.mid")