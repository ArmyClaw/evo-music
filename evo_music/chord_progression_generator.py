"""
和弦进行生成器 - 自动生成经典和弦进行
"""

import random
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .notes import NoteName
from .chords import Chord, ChordFactory, ChordType, ChordProgressionAnalyzer
from .scales import Scale, ScaleFactory


class ProgressionStyle(Enum):
    """和弦进行风格"""
    CLASSIC_POP = "classic_pop"      # 经典流行：I-V-vi-IV
    JAZZ_STANDARD = "jazz_standard" # 爵士标准：ii-V-I
    BLUES_12_BAR = "blues_12_bar"   # 12小节布鲁斯
    ROMANTIC = "romantic"           # 浪漫主义：I-IV-vi-iii-V-vi-IV-I-IV
    ROCK = "rock"                   # 摇滚：I-IV-V
    FOLK = "folk"                   # 民谣：I-V-vi-IV
    GOSPEL = "gospel"               # 福音：I-IV-I-V
    MODERN = "modern"               # 现代：vi-IV-I-V
    
    @classmethod
    def get_styles(cls) -> List['ProgressionStyle']:
        """获取所有可用风格"""
        return list(cls)
    
    @classmethod
    def get_description(cls, style: 'ProgressionStyle') -> str:
        """获取风格描述"""
        descriptions = {
            ProgressionStyle.CLASSIC_POP: "经典流行和弦进行（I-V-vi-IV）",
            ProgressionStyle.JAZZ_STANDARD: "爵士标准和弦进行（ii-V-I）",
            ProgressionStyle.BLUES_12_BAR: "12小节布鲁斯进行",
            ProgressionStyle.ROMANTIC: "浪漫主义复杂和弦进行",
            ProgressionStyle.ROCK: "简单摇滚进行（I-IV-V）",
            ProgressionStyle.FOLK: "民谣流行进行（I-V-vi-IV）",
            ProgressionStyle.GOSPEL: "福音音乐进行（I-IV-I-V）",
            ProgressionStyle.MODERN: "现代流行进行（vi-IV-I-V）"
        }
        return descriptions.get(style, "未知风格")


@dataclass
class ChordProgressionTemplate:
    """和弦进行模板"""
    name: str
    style: ProgressionStyle
    chord_functions: List[str]  # 功能标记列表，如 ["I", "IV", "V"]
    chord_types: List[str]      # 和弦类型列表，如 ["major", "major", "major"]
    description: str
    complexity: int = 1  # 复杂度等级 1-5
    popularity: float = 0.5  # 流行度 0.0-1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "style": self.style.value,
            "chord_functions": self.chord_functions,
            "chord_types": self.chord_types,
            "description": self.description,
            "complexity": self.complexity,
            "popularity": self.popularity
        }


class ChordProgressionGenerator:
    """和弦进行生成器"""
    
    # 预定义的和弦进行模板
    PROGRESSION_TEMPLATES = [
        ChordProgressionTemplate(
            name="经典流行",
            style=ProgressionStyle.CLASSIC_POP,
            chord_functions=["I", "V", "vi", "IV"],
            chord_types=["major", "major", "minor", "major"],
            description="最流行的和弦进行之一，广泛应用于流行音乐",
            complexity=1,
            popularity=0.95
        ),
        ChordProgressionTemplate(
            name="爵士标准",
            style=ProgressionStyle.JAZZ_STANDARD,
            chord_functions=["ii", "V", "I"],
            chord_types=["minor7", "dominant7", "major7"],
            description="爵士音乐最经典的进行",
            complexity=2,
            popularity=0.9
        ),
        ChordProgressionTemplate(
            name="简单摇滚",
            style=ProgressionStyle.ROCK,
            chord_functions=["I", "IV", "V"],
            chord_types=["major", "major", "major"],
            description="简单明了的摇滚进行",
            complexity=1,
            popularity=0.8
        ),
        ChordProgressionTemplate(
            name="12小节布鲁斯",
            style=ProgressionStyle.BLUES_12_BAR,
            chord_functions=["I", "IV", "I", "IV", "I", "V", "IV", "I"],
            chord_types=["dominant7", "dominant7", "dominant7", "dominant7", 
                        "dominant7", "dominant7", "dominant7", "dominant7"],
            description="传统的12小节布鲁斯进行",
            complexity=1,
            popularity=0.7
        ),
        ChordProgressionTemplate(
            name="浪漫主义",
            style=ProgressionStyle.ROMANTIC,
            chord_functions=["I", "IV", "vi", "iii", "V", "vi", "IV", "I", "IV", "V"],
            chord_types=["major", "major", "minor", "minor", "major", "minor", "major", "major", "major", "major"],
            description="复杂浪漫主义的进行，情感丰富",
            complexity=4,
            popularity=0.6
        ),
        ChordProgressionTemplate(
            name="现代流行",
            style=ProgressionStyle.MODERN,
            chord_functions=["vi", "IV", "I", "V"],
            chord_types=["minor", "major", "major", "major"],
            description="现代流行音乐的常用进行",
            complexity=2,
            popularity=0.85
        ),
        ChordProgressionTemplate(
            name="福音",
            style=ProgressionStyle.GOSPEL,
            chord_functions=["I", "IV", "I", "V"],
            chord_types=["major", "major", "major", "major"],
            description="福音音乐经典进行",
            complexity=1,
            popularity=0.75
        ),
        ChordProgressionTemplate(
            name="小调流行",
            style=ProgressionStyle.FOLK,
            chord_functions=["i", "VI", "III", "VII"],
            chord_types=["minor", "major", "major", "major"],
            description="小调流行进行",
            complexity=2,
            popularity=0.7
        )
    ]
    
    def __init__(self):
        self.scale_cache = {}
    
    def generate_progression(self, 
                           root_note: str, 
                           scale_type: str = "major",
                           style: ProgressionStyle = ProgressionStyle.CLASSIC_POP,
                           length: int = 4,
                           variation: float = 0.1) -> List[Chord]:
        """
        生成和弦进行
        
        Args:
            root_note: 根音（如 "C", "G"）
            scale_type: 音阶类型（如 "major", "minor"）
            style: 和弦进行风格
            length: 进行长度（小节数）
            variation: 变化程度（0.0-1.0）
            
        Returns:
            和弦列表
        """
        # 解析根音
        root_note_obj = NoteName.from_string(root_note)
        
        # 创建音阶
        scale = self._get_scale(root_note_obj, scale_type)
        
        # 根据风格选择模板
        template = self._get_template_by_style(style)
        
        # 生成和弦进行
        progression = self._build_progression_from_template(
            template, scale, length, variation
        )
        
        return progression
    
    def generate_multiple_progressions(self, 
                                    root_note: str,
                                    scale_type: str = "major",
                                    styles: Optional[List[ProgressionStyle]] = None,
                                    count: int = 5,
                                    length: int = 4) -> Dict[ProgressionStyle, List[Chord]]:
        """
        生成多种风格的和弦进行
        
        Args:
            root_note: 根音
            scale_type: 音阶类型
            styles: 指定风格列表，None表示使用所有风格
            count: 每种风格的生成数量
            length: 进行长度
            
        Returns:
            {风格: 和弦列表} 的字典
        """
        if styles is None:
            styles = ProgressionStyle.get_styles()
        
        results = {}
        
        for style in styles:
            progressions = []
            for _ in range(count):
                progression = self.generate_progression(
                    root_note, scale_type, style, length
                )
                progressions.append(progression)
            results[style] = progressions
        
        return results
    
    def get_random_progression(self, 
                             root_note: str,
                             scale_type: str = "major",
                             length: int = 4) -> List[Chord]:
        """生成随机和弦进行"""
        styles = ProgressionStyle.get_styles()
        style = random.choice(styles)
        return self.generate_progression(root_note, scale_type, style, length)
    
    def analyze_progression_tension(self, progression: List[Chord]) -> Dict[str, Any]:
        """分析和弦进行的紧张度"""
        analysis = ChordProgressionAnalyzer.analyze_progression(progression)
        
        # 计算紧张度指标
        tension_metrics = {
            "seventh_chord_ratio": sum(1 for chord in progression if chord.is_seventh_chord()) / len(progression) if progression else 0,
            "tritone_distance": self._calculate_tritone_distance(progression),
            "chromatic_movement": self._calculate_chromatic_movement(progression),
            "overall_tension": analysis.get("tension_level", 0)
        }
        
        return {
            "basic_analysis": analysis,
            "tension_metrics": tension_metrics,
            "tension_level": self._calculate_total_tension(tension_metrics)
        }
    
    def suggest_improvements(self, progression: List[Chord]) -> List[str]:
        """建议和弦进行改进"""
        suggestions = []
        
        # 检查是否太简单
        if len(progression) < 3:
            suggestions.append("考虑增加和弦数量以丰富和声")
        
        # 检查紧张度
        tension_analysis = self.analyze_progression_tension(progression)
        if tension_analysis["tension_level"] < 0.3:
            suggestions.append("考虑加入七和弦增加紧张度")
        
        # 检查音程运动
        root_movement = [abs(progression[i+1].root_note.value - progression[i].root_note.value) 
                        for i in range(len(progression)-1)]
        
        if all(movement <= 2 for movement in root_movement):
            suggestions.append("考虑增加根音距离创造更多变化")
        
        # 检查和弦类型多样性
        chord_types = set(chord.chord_type for chord in progression)
        if len(chord_types) == 1:
            suggestions.append("考虑加入不同类型的和弦增加色彩")
        
        return suggestions
    
    # ============ 私有方法 ============
    
    def _get_scale(self, root_note: NoteName, scale_type: str) -> Scale:
        """获取音阶"""
        cache_key = f"{root_note.value_str}_{scale_type}"
        if cache_key not in self.scale_cache:
            self.scale_cache[cache_key] = ScaleFactory.create_scale(root_note, scale_type)
        return self.scale_cache[cache_key]
    
    def get_template_by_style(self, style: ProgressionStyle) -> ChordProgressionTemplate:
        """根据风格获取模板"""
        for template in self.PROGRESSION_TEMPLATES:
            if template.style == style:
                return template
        
        # 如果没有找到，返回默认模板
        return self.PROGRESSION_TEMPLATES[0]
    
    def _get_template_by_style(self, style: ProgressionStyle) -> ChordProgressionTemplate:
        """根据风格获取模板（内部使用）"""
        return self.get_template_by_style(style)
    
    def _build_progression_from_template(self, 
                                       template: ChordProgressionTemplate,
                                       scale: Scale,
                                       length: int,
                                       variation: float) -> List[Chord]:
        """根据模板构建和弦进行"""
        progression = []
        
        # 获取音阶中的和弦
        scale_chords = self._get_scale_chords(scale)
        
        # 扩展模板到指定长度
        extended_functions = template.chord_functions * (length // len(template.chord_functions) + 1)
        extended_functions = extended_functions[:length]
        
        # 为每个功能标记创建和弦
        for func in extended_functions:
            # 查找对应功能的和弦
            chord = self._find_chord_by_function(func, scale_chords, template.chord_types)
            
            # 应用变化
            if variation > 0 and random.random() < variation:
                chord = self._apply_variation(chord, scale)
            
            progression.append(chord)
        
        return progression
    
    def _get_scale_chords(self, scale: Scale) -> List[Chord]:
        """获取音阶中的和弦"""
        chords = []
        roman_numerals = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
        
        for i, note in enumerate(scale.notes):
            # 根据音阶位置确定和弦类型
            if scale.scale_type == "major":
                if i == 0 or i == 3 or i == 4:  # I, IV, V
                    chord_type = ChordType.MAJOR
                elif i == 1 or i == 6:  # ii, vii°
                    chord_type = ChordType.DIMINISHED if i == 6 else ChordType.MINOR
                else:  # iii, vi
                    chord_type = ChordType.MINOR
            else:  # minor
                if i == 0 or i == 3 or i == 4:
                    chord_type = ChordType.MINOR
                elif i == 1 or i == 5:
                    chord_type = ChordType.DIMINISHED if i == 1 else ChordType.MAJOR
                elif i == 2:
                    chord_type = ChordType.AUGMENTED
                else:  # vii°
                    chord_type = ChordType.DIMINISHED
            
            chord = ChordFactory.create_triad(note, chord_type)
            chord.function = roman_numerals[i]
            chords.append(chord)
        
        return chords
    
    def _find_chord_by_function(self, function: str, scale_chords: List[Chord], chord_types: List[str]) -> Chord:
        """根据功能标记查找和弦"""
        # 首先尝试找到完全匹配的和弦
        for chord in scale_chords:
            if chord.function == function:
                return chord
        
        # 如果没有找到，根据功能类型创建和弦
        function_to_note_index = {
            "I": 0, "ii": 1, "iii": 2, "IV": 3, "V": 4, "vi": 5, "vii°": 6
        }
        
        if function in function_to_note_index:
            note_index = function_to_note_index[function]
            root_note = NoteName(note_index % 12)  # 简化处理
            
            # 获取对应的和弦类型
            chord_type_index = note_index % len(chord_types)
            chord_type = chord_types[chord_type_index]
            
            chord = ChordFactory.create_chord(root_note, chord_type)
            chord.function = function
            return chord
        
        # 默认返回I和弦
        return ChordFactory.create_triad(NoteName.C, ChordType.MAJOR)
    
    def _apply_variation(self, chord: Chord, scale: Scale) -> Chord:
        """应用和弦变化"""
        variations = []
        
        # 尝试转为七和弦
        if random.random() < 0.3:
            if chord.chord_type == ChordType.MAJOR:
                variations.append(ChordType.MAJOR7)
            elif chord.chord_type == ChordType.MINOR:
                variations.append(ChordType.MINOR7)
            elif chord.chord_type == ChordType.DIMINISHED:
                variations.append(ChordType.DIMINISHED7)
        
        # 尝试添加转位
        if random.random() < 0.2 and chord.get_inversions():
            inversions = chord.get_inversions()
            if inversions:
                return random.choice(inversions)
        
        # 应用变化
        if variations:
            return ChordFactory.create_chord(chord.root_note, variations[0])
        
        return chord
    
    def _calculate_tritone_distance(self, progression: List[Chord]) -> float:
        """计算三全音距离"""
        distances = []
        
        for i in range(len(progression) - 1):
            current = progression[i]
            next_chord = progression[i + 1]
            
            # 计算根音距离
            distance = abs(next_chord.root_note.value - current.root_note.value)
            distances.append(min(distance, 12 - distance))
        
        return sum(distances) / len(distances) if distances else 0
    
    def _calculate_chromatic_movement(self, progression: List[Chord]) -> float:
        """计算半音运动"""
        chromatic_count = 0
        
        for i in range(len(progression) - 1):
            current = progression[i]
            next_chord = progression[i + 1]
            
            # 检查是否为半音关系
            movement = abs(next_chord.root_note.value - current.root_note.value)
            if movement == 1:
                chromatic_count += 1
        
        return chromatic_count / (len(progression) - 1) if len(progression) > 1 else 0
    
    def _calculate_total_tension(self, tension_metrics: Dict[str, float]) -> float:
        """计算总紧张度"""
        weights = {
            "seventh_chord_ratio": 0.4,
            "tritone_distance": 0.3,
            "chromatic_movement": 0.2,
            "overall_tension": 0.1
        }
        
        total_tension = 0
        for metric, weight in weights.items():
            total_tension += tension_metrics.get(metric, 0) * weight
        
        return min(total_tension, 1.0)
    
    # ============ 工具方法 ============
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """列出所有模板"""
        return [template.to_dict() for template in self.PROGRESSION_TEMPLATES]
    
    def get_template_by_name(self, name: str) -> Optional[ChordProgressionTemplate]:
        """根据名称获取模板"""
        for template in self.PROGRESSION_TEMPLATES:
            if template.name == name:
                return template
        return None
    
    def export_progressions(self, progressions: Dict[ProgressionStyle, List[List[Chord]]], 
                          filename: str = "progressions.json") -> None:
        """导出和弦进行"""
        import json
        
        data = {}
        for style, prog_list in progressions.items():
            data[style.value] = [
                [chord.to_dict() for chord in progression] 
                for progression in prog_list
            ]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_progressions(self, filename: str) -> Dict[ProgressionStyle, List[List[Chord]]]:
        """导入和弦进行"""
        import json
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = {}
        for style_str, prog_list in data.items():
            try:
                style = ProgressionStyle(style_str)
                progressions = []
                
                for chord_data in prog_list:
                    # 这里需要根据chord_data重建Chord对象
                    # 简化处理，实际应用中需要更完整的序列化/反序列化
                    progressions.append([])  # 临时空列表
                
                results[style] = progressions
            except ValueError:
                continue
        
        return results


# ============ 全局实例 ============
progression_generator = ChordProgressionGenerator()


# ============ 快捷函数 ============

def generate_progression(root_note: str, 
                        scale_type: str = "major",
                        style: ProgressionStyle = ProgressionStyle.CLASSIC_POP,
                        length: int = 4,
                        variation: float = 0.1) -> List[Chord]:
    """快捷函数：生成和弦进行"""
    return progression_generator.generate_progression(root_note, scale_type, style, length, variation)

def generate_multiple_progressions(root_note: str,
                                  scale_type: str = "major",
                                  styles: Optional[List[ProgressionStyle]] = None,
                                  count: int = 5,
                                  length: int = 4) -> Dict[ProgressionStyle, List[Chord]]:
    """快捷函数：生成多种风格的和弦进行"""
    return progression_generator.generate_multiple_progressions(root_note, scale_type, styles, count, length)

def get_random_progression(root_note: str,
                          scale_type: str = "major",
                          length: int = 4) -> List[Chord]:
    """快捷函数：生成随机和弦进行"""
    return progression_generator.get_random_progression(root_note, scale_type, length)


if __name__ == "__main__":
    # 运行演示
    print("=== 和弦进行生成器演示 ===")
    
    # 生成经典流行进行
    classic_pop = generate_progression("C", "major", ProgressionStyle.CLASSIC_POP, 4)
    print(f"经典流行进行 (C大调): {[chord.name for chord in classic_pop]}")
    
    # 生成爵士进行
    jazz = generate_progression("C", "major", ProgressionStyle.JAZZ_STANDARD, 3)
    print(f"爵士进行 (C大调): {[chord.name for chord in jazz]}")
    
    # 生成随机进行
    random_prog = get_random_progression("G", "major", 4)
    print(f"随机进行 (G大调): {[chord.name for chord in random_prog]}")
    
    # 分析紧张度
    tension_analysis = progression_generator.analyze_progression_tension(classic_pop)
    print(f"经典流行进行紧张度: {tension_analysis['tension_level']:.2f}")
    
    # 获取建议
    suggestions = progression_generator.suggest_improvements(classic_pop)
    print(f"改进建议: {suggestions}")