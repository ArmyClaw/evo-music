"""
Evo Music - 自进化音乐引擎
Phase 1: Music Theory 基础数据模型
Phase 2: Melody Generation 旋律生成
"""

from .rhythm_patterns import RhythmLibrary
from .melody import MarkovMelodyGenerator, MelodyConfig, generate_melody

__version__ = "0.2.0"
__author__ = "ArmyClaw"