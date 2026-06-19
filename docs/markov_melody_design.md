# 马尔可夫链旋律生成算法设计

## 概述
设计基于马尔可夫链的旋律生成系统，通过统计音程转换概率来生成连贯的旋律线条。

## 系统架构

### 1. 数据结构设计

#### MelodyState
```python
@dataclass
class MelodyState:
    """旋律状态"""
    current_note: NoteName           # 当前音符
    current_scale: Scale             # 当前音阶
    octave: int                     # 当前八度
    velocity: int                   # 当前力度
    note_duration: float            # 当前音符时值
```

#### TransitionMatrix
```python
@dataclass
class TransitionMatrix:
    """音程转换概率矩阵"""
    scale_type: str                 # 音阶类型
    matrix: Dict[Tuple[int, int], float]  # (from_note, to_note) -> 概率
    note_durations: Dict[float, float]    # 时值转移概率
    
    @staticmethod
    def from_scale(scale: Scale) -> 'TransitionMatrix':
        """从音阶创建转换矩阵"""
        
    def get_next_note(self, current_note: int) -> NoteName:
        """根据当前音符获取下一个音符"""
        
    def get_next_duration(self, current_duration: float) -> float:
        """获取下一个音符时值"""
```

### 2. 马尔可夫链生成器

#### MarkovMelodyGenerator
```python
class MarkovMelodyGenerator:
    """马尔可夫链旋律生成器"""
    
    def __init__(self, transition_matrix: TransitionMatrix):
        self.matrix = transition_matrix
        self.current_state = None
        self.sequence = []
        
    def start(self, scale: Scale, start_note: NoteName, octave: int = 4):
        """开始生成序列"""
        self.current_state = MelodyState(
            current_note=start_note,
            current_scale=scale,
            octave=octave,
            velocity=80,
            note_duration=1.0
        )
        self.sequence = [self.current_state]
        
    def generate_step(self) -> MelodyState:
        """生成下一步旋律"""
        next_note = self.matrix.get_next_note(self.current_state.current_note.value)
        next_duration = self.matrix.get_next_duration(self.current_state.note_duration)
        
        # 八度跳跃控制
        octave_change = self._calculate_octave_jump()
        next_octave = self.current_state.octave + octave_change
        
        # 力度变化
        next_velocity = self._calculate_velocity_change()
        
        self.current_state = MelodyState(
            current_note=next_note,
            current_scale=self.current_state.current_scale,
            octave=next_octave,
            velocity=next_velocity,
            note_duration=next_duration
        )
        
        self.sequence.append(self.current_state)
        return self.current_state
        
    def generate_sequence(self, length: int) -> List[MelodyState]:
        """生成完整序列"""
        for _ in range(length):
            self.generate_step()
        return self.sequence
    
    def _calculate_octave_jump(self) -> int:
        """计算八度跳跃"""
        # 基于概率的八度变化策略
        pass
        
    def _calculate_velocity_change(self) -> int:
        """计算力度变化"""
        # 基于旋律轮廓的力度变化
        pass
```

### 3. 训练系统

#### MelodyTrainer
```python
class MelodyTrainer:
    """旋律训练器 - 从现有旋律学习转换概率"""
    
    def __init__(self, scale_type: str):
        self.scale_type = scale_type
        self.note_transitions = defaultdict(int)
        self.duration_transitions = defaultdict(int)
        self.total_notes = 0
        
    def train_from_melody(self, melody: List[NoteName]):
        """从旋律序列训练"""
        for i in range(len(melody) - 1):
            current = melody[i].value
            next_note = melody[i + 1].value
            self.note_transitions[(current, next_note)] += 1
            self.total_notes += 1
            
    def train_from_midi(self, midi_file: str):
        """从MIDI文件训练"""
        # 解析MIDI文件并提取旋律
        pass
        
    def build_transition_matrix(self) -> TransitionMatrix:
        """构建转换矩阵"""
        matrix = {}
        for (from_note, to_note), count in self.note_transitions.items():
            probability = count / self.total_notes
            matrix[(from_note, to_note)] = probability
            
        return TransitionMatrix(
            scale_type=self.scale_type,
            matrix=matrix,
            note_durations=self._build_duration_matrix()
        )
```

### 4. 情感映射

#### EmotionMapper
```python
class EmotionMapper:
    """情感与音阶映射系统"""
    
    EMOTION_SCALE_MAP = {
        'happy': ScaleType.MAJOR,
        'sad': ScaleType.NATURAL_MINOR,
        'mysterious': ScaleType.LOCRIAN,
        'epic': ScaleType.PHRYGIAN,
        'peaceful': ScaleType.LYDIAN,
        'dark': ScaleType.HARMONIC_MINOR,
        'bright': ScaleType.MAJOR,
        'chinese': ScaleType.CHINESE_MAJOR,
        'blues': ScaleType.BLUES_MINOR
    }
    
    @staticmethod
    def get_scale_for_emotion(emotion: str, root_note: NoteName = NoteName.C) -> Scale:
        """根据情感获取对应音阶"""
        scale_type = EMOTION_SCALE_MAP.get(emotion, ScaleType.MAJOR)
        return Scale.create(root_note, scale_type)
        
    @staticmethod
    def get_emotion_from_scale(scale: Scale) -> str:
        """从音阶推断情感"""
        # 简化的情感推断逻辑
        scale_to_emotion = {v: k for k, v in EMOTION_SCALE_MAP.items()}
        return scale_to_emotion.get(scale.scale_type, 'neutral')
```

### 5. 旋律连贯性优化

#### MelodyOptimizer
```python
class MelodyOptimizer:
    """旋律连贯性优化器"""
    
    def __init__(self, generator: MarkovMelodyGenerator):
        self.generator = generator
        
    def optimize_leaps(self, max_leap: int = 7) -> List[MelodyState]:
        """优化音程跳跃"""
        for i, state in enumerate(self.generator.sequence[1:], 1):
            prev_note = self.generator.sequence[i-1].current_note.value
            current_note = state.current_note.value
            
            leap = abs(current_note - prev_note)
            if leap > max_leap:
                # 修复大跳
                state.current_note = self._find_closest_note(
                    current_note, prev_note, state.current_scale
                )
                
    def optimize_climax_placement(self, climax_position: float = 0.7) -> List[MelodyState]:
        """优化高潮位置"""
        melody_length = len(self.generator.sequence)
        climax_index = int(melody_length * climax_position)
        
        # 在高潮位置设置高音和强力度
        for i, state in enumerate(self.generator.sequence):
            if abs(i - climax_index) < 3:  # 高潮附近
                state.velocity = min(127, state.velocity + 20)
                if state.current_note.value > 7:  # 高音区
                    state.velocity = min(127, state.velocity + 10)
                    
    def _find_closest_note(self, target: int, reference: int, scale: Scale) -> NoteName:
        """寻找最近的音阶内音符"""
        # 实现寻找最近音阶音符的逻辑
        pass
```

## 算法流程

### 1. 初始化
```python
# 创建训练器
trainer = MelodyTrainer("major")

# 训练现有旋律数据
trainer.train_from_midi("existing_melodies.mid")

# 构建转换矩阵
matrix = trainer.build_transition_matrix()

# 创建生成器
generator = MarkovMelodyGenerator(matrix)
```

### 2. 生成旋律
```python
# 设置情感和音阶
emotion = "happy"
scale = EmotionMapper.get_scale_for_emotion(emotion, NoteName.C)

# 开始生成
generator.start(scale, NoteName.C, octave=4)

# 生成序列
melody = generator.generate_sequence(length=32)

# 优化旋律
optimizer = MelodyOptimizer(generator)
optimizer.optimize_leaps()
optimizer.optimize_climax_placement()
```

### 3. 输出
```python
# 转换为MIDI
midi_output = convert_to_midi(melody)
midi_output.save("generated_melody.mid")

# 或者转换为音符序列
note_sequence = [state.current_note.value_str for state in melody]
print("Generated melody:", note_sequence)
```

## 性能优化

### 1. 矩阵缓存
```python
class MatrixCache:
    """转换矩阵缓存"""
    
    @lru_cache(maxsize=32)
    def get_matrix(self, scale_type: str, root_note: int) -> TransitionMatrix:
        """获取缓存的转换矩阵"""
        pass
```

### 2. 并行生成
```python
def generate_parallel_scales(emotions: List[str]) -> Dict[str, List[MelodyState]]:
    """并行生成不同情感的旋律"""
    with ThreadPoolExecutor() as executor:
        futures = []
        for emotion in emotions:
            future = executor.submit(generate_for_emotion, emotion)
            futures.append(future)
        
        return {emotion: future.result() for emotion, future in zip(emotions, futures)}
```

## 测试策略

### 1. 单元测试
- 转换矩阵正确性测试
- 音阶约束测试
- 八度跳跃边界测试
- 情感映射测试

### 2. 集成测试
- 完整生成流程测试
- MIDI输出测试
- 多情感对比测试

### 3. 听觉测试
- 生成旋律的连贯性评估
- 不同情感的区分度评估
- 旋律自然度评估

## 扩展性设计

### 1. 支持更多音阶
- 添加民族音阶训练数据
- 支持自定义音阶模式
- 异音阶转换支持

### 2. 高级特征
- 节奏模式集成
- 动态力度变化
- 滑音效果
- 装饰音生成

### 3. 机器学习集成
- 深度学习模型替换
- 强化学习优化
- 用户偏好学习

## 实现优先级

### Phase 1: 基础实现
- [x] 马尔可夫链核心算法
- [x] 音阶约束支持
- [x] 基础MIDI输出

### Phase 2: 增强功能
- [ ] 情感映射系统
- [ ] 旋律连贯性优化
- [ ] 训练系统实现

### Phase 3: 高级特性
- [ ] 并行生成
- [ ] 缓存机制
- [ ] 机器学习集成

## 性能指标

- 生成速度：100个音符/秒
- 内存占用：< 10MB（包含缓存）
- 支持音阶数量：>20种
- 生成质量：85%以上自然度