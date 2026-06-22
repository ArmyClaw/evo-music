# 🧬 Evo Music — 自进化音乐引擎

> 从乐理基础到自主创作，AI 的音乐进化之路。马尔可夫链生成旋律 + 遗传算法进化优化。

## 在线地址

- **项目展示**: https://army-yorozuya.art/study/evo-music/
- **简易播放器**: https://army-yorozuya.art/study/evo-music/web_player.html

> ⚠️ Web 播放器功能有限，完整引擎需本地运行。

## 完成进度

| 阶段 | 内容 | 状态 |
|---|---|---|
| Phase 1 | 乐理基础（音阶、和弦、节奏） | ✅ 完成 |
| Phase 2 | 旋律生成（马尔可夫链、情感映射） | ✅ 完成 |
| Phase 3 | 编曲引擎（多声部、曲式、鼓点） | ✅ 完成 |
| Phase 4 | 进化机制（遗传算法、适应度优化） | ✅ 完成 |

## 源码结构

```
evo-music/
├── evo_music/                  # 核心引擎包
│   ├── __init__.py
│   ├── notes.py                # 音符/音阶定义
│   ├── scales.py               # 调式系统
│   ├── chords.py               # 和弦进行
│   ├── rhythm.py               # 节奏模式
│   ├── rhythm_patterns.py      # 鼓点模式库
│   ├── melody.py               # 旋律生成（马尔可夫链）
│   ├── melody_optimizer.py     # 旋律优化
│   ├── music_theory.py         # 乐理规则
│   ├── harmony_arranger.py     # 和声编排
│   ├── chord_progression_generator.py  # 和弦进行生成
│   ├── drum_layer.py           # 鼓组层
│   ├── form_structure.py       # 曲式结构（A-B-A）
│   ├── emotion_mapping.py      # 情感→调式映射
│   ├── fitness.py              # 适应度函数
│   ├── genetic_algorithm.py    # 遗传算法引擎
│   └── midi_output.py          # MIDI 文件输出
├── simple_demo.py              # 简单演示
├── genetic_demo.py             # 遗传算法演示
├── evo-markov-demo.py          # 马尔可夫旋律演示
├── evolution_iteration.py      # 进化迭代（多代收敛）
├── generate_aba_form.py         # A-B-A 曲式生成
├── evolve_melodies.py          # 进化旋律主程序
├── test_and_verify.py          # 完整测试套件
└── web_player.html             # 简易 Web 播放器
```

## 本地运行

```bash
cd ~/projects/evo-music

# 简单演示 — 生成一段旋律
python3 simple_demo.py

# 马尔可夫链旋律生成
python3 evo-markov-demo.py

# 遗传算法进化 — 多代迭代收敛到高分旋律
python3 genetic_demo.py

# 进化迭代 — 完整进化流程
python3 evolution_iteration.py

# A-B-A 曲式生成
python3 generate_aba_form.py

# 和声编排测试
python3 test_harmony_arrangement.py

# 和弦进行生成
python3 test_chord_progression.py

# 运行完整测试
python3 test_and_verify.py

# 情感映射演示
python3 emotion_mapping_demo.py
```

## 引擎 API（Python）

```python
from evo_music.melody import MarkovMelodyGenerator
from evo_music.genetic_algorithm import GeneticEvolver
from evo_music.midi_output import MidiOutput

# 1. 马尔可夫链生成旋律
gen = MarkovMelodyGenerator(key='C', mode='major')
melody = gen.generate(num_notes=32)

# 2. 遗传算法进化
evolver = GeneticEvolver(
    population_size=20,
    mutation_rate=0.1,
    generations=50
)
best_melody = evolver.evolve()

# 3. 输出 MIDI
midi = MidiOutput()
midi.add_melody(best_melody)
midi.save('output.mid')
```

## 技术栈

- **引擎**: Python 3 + MIDIUtil
- **旋律生成**: 马尔可夫链
- **进化优化**: 遗传算法（选择/交叉/变异/精英保留）
- **输出**: MIDI 文件
- **Web 播放**: Web Audio API（简化版）

## 下一步

- [ ] FastAPI Web 服务化
- [ ] 完整前端播放器（进度条、调式选择、进化控制）
- [ ] Web Audio API 实时合成（无需 MIDI）
- [ ] 多风格预设

🌱 2026-06-17 开工
