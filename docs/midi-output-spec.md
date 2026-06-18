# MIDI输出规范

## 概述
本文档定义了evo-music项目的MIDI输出规范，包括文件格式要求和输出接口设计。

## 文件格式要求

### 文件扩展名
- `.mid` - 标准MIDI格式
- `.midi` - 可选的替代扩展名

### 文件结构
```
evo-music-output/
├── midi/
│   ├── compositions/         # 完整作品
│   │   ├── piece-name.mid
│   │   └── piece-name_info.txt
│   ├── patterns/            # 循环节拍
│   │   ├── pattern-name.mid
│   │   └── pattern-name_info.txt
│   └── experiments/         # 实验性输出
│       ├── experiment-name.mid
│       └── experiment-name_info.txt
└── metadata/                # 元数据文件
    ├── compositions.json    # 作品元数据
    ├── patterns.json       # 节拍元数据
    └── experiments.json    # 实验元数据
```

### MIDI轨道结构
1. **节奏轨道** (Track 1) - 打击乐和基础节拍
2. **和声轨道** (Track 2) - 和弦和伴奏
3. **旋律轨道** (Track 3) - 主要旋律线
4. **贝斯轨道** (Track 4) - 低音线
5. **特效轨道** (Track 5) - 音效和特殊处理

### 元数据格式
每个MIDI文件应包含对应的元数据文件，格式为JSON：

```json
{
  "title": "作品名称",
  "composer": "evo-music AI",
  "created_at": "2026-06-17T21:00:00Z",
  "duration_seconds": 180,
  "tempo": 120,
  "time_signature": "4/4",
  "key_signature": "C Major",
  "description": "作品描述",
  "tags": ["experimental", "ambient", "generative"],
  "parameters": {
    "complexity": 0.7,
    "harmony_level": 0.8,
    "rhythm_intensity": 0.6
  }
}
```

## 输出接口

### 主要输出函数

```python
def generate_midi(composition_data, output_path, metadata=None):
    """
    生成MIDI文件
    
    Args:
        composition_data (dict): 包含音乐数据的字典
        output_path (str): 输出文件路径
        metadata (dict): 可选的元数据
    """
    pass

def export_compositions(compositions, directory, format='midi'):
    """
    导出多个作品
    
    Args:
        compositions (list): 作品数据列表
        directory (str): 输出目录
        format (str): 输出格式 ('midi', 'mp3', 'wav')
    """
    pass

def validate_midi_structure(midi_path):
    """
    验证MIDI文件结构
    
    Args:
        midi_path (str): MIDI文件路径
        
    Returns:
        bool: 验证结果
        list: 错误信息列表
    """
    pass
```

### 数据结构定义

#### Composition数据结构
```python
{
  "id": "unique_id",
  "title": "作品名称",
  "structure": {
    "intro": {"bars": 4, "tempo": 80},
    "verse": {"bars": 8, "tempo": 120},
    "chorus": {"bars": 16, "tempo": 140},
    "bridge": {"bars": 8, "tempo": 100},
    "outro": {"bars": 4, "tempo": 80}
  },
  "instruments": {
    "rhythm": ["acoustic_drum", "electric_bass"],
    "harmony": ["piano", "synth_pad"],
    "melody": ["violin", "flute"]
  },
  "notes": [
    {
      "track": 1,
      "time": 0,
      "duration": 0.5,
      "pitch": 60,
      "velocity": 80,
      "channel": 9
    }
  ]
}
```

## 音色映射

### GM标准音色映射
- 钢琴: 0-7, 16-23
- 吉他: 24-31
- 贝斯: 32-39
- 弦乐: 40-47
- 铜管: 56-63
- 打击乐: 0-127 (GM打击乐区)

### 专用音色
- 电子音色: 100-127
- 实验音效: 128-255 (扩展范围)

## 质量标准

1. **节拍准确性**: ±2ms 误差
2. **音高精确度**: ±1 semitone
3. **动态范围**: 0-127 (MIDI标准)
4. **文件大小**: 单个作品不超过10MB
5. **兼容性**: 兼容标准MIDI播放器和DAW软件

## 错误处理

- 文件创建失败时自动重试3次
- 验证失败时返回详细错误信息
- 内存溢出时优雅降级处理

## 版本控制

- 所有MIDI文件纳入Git版本控制
- 元数据文件定期同步到中央数据库
- 支持增量更新和差异对比