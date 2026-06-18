"""
节奏模式库 - 常用节奏pattern集合
覆盖拍号: 4/4, 3/4, 2/4, 6/8, 12/8, 5/4, 7/8
覆盖风格: Pop, Rock, Jazz, Funk, Latin, Reggae, Electronic, Blues, Waltz, Ballad, Disco, Hip-Hop, R&B, Metal, Country, Folk

每个模式以一小节为单位，可自由重复和组合。
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from .rhythm import (
    TimeSignature, NoteDuration, NoteEvent, RhythmPattern, RhythmFactory
)


# ============================================================
# 4/4 拍模式库（最常用）
# ============================================================

def _4_4_basic_pop() -> RhythmPattern:
    """流行基本：四分音符均匀分布"""
    events = [NoteEvent(None, 1.0, vel, dotted=False) for vel in [90, 70, 80, 70]]
    return RhythmPattern("4/4 Basic Pop", TimeSignature.FOUR_FOUR, events, 120,
                         "流行基本节奏：四分音符均匀，强-弱-次强-弱")

def _4_4_eighth_pop() -> RhythmPattern:
    """流行八分音符"""
    vels = [90, 60, 70, 60, 80, 60, 70, 60]
    events = [NoteEvent(None, 0.5, v) for v in vels]
    return RhythmPattern("4/4 Eighth Pop", TimeSignature.FOUR_FOUR, events, 120,
                         "八分音符流行节奏")

def _4_4_rock_steady() -> RhythmPattern:
    """摇滚稳定节拍：底鼓+军鼓交替"""
    events = [
        NoteEvent(None, 0.5, 100),   # 底鼓
        NoteEvent(None, 0.5, 50),    # 踩镲
        NoteEvent(None, 0.5, 95),    # 军鼓
        NoteEvent(None, 0.5, 50),    # 踩镲
        NoteEvent(None, 0.5, 100),   # 底鼓
        NoteEvent(None, 0.5, 50),    # 踩镲
        NoteEvent(None, 0.5, 95),    # 军鼓
        NoteEvent(None, 0.5, 50),    # 踩镲
    ]
    return RhythmPattern("4/4 Rock Steady", TimeSignature.FOUR_FOUR, events, 120,
                         "摇滚稳定节拍：底鼓-踩镲-军鼓-踩镲 x2")

def _4_4_jazz_swing() -> RhythmPattern:
    """爵士摇摆：swing八分音符（2:1比例）"""
    # swing feel: 长短交替 0.67 + 0.33
    pairs = [(0.67, 80, "ride"), (0.33, 55, "ride")] * 4
    events = [NoteEvent(None, d, v) for d, v, _ in pairs]
    return RhythmPattern("4/4 Jazz Swing", TimeSignature.FOUR_FOUR, events, 140,
                         "爵士摇摆节奏：swing八分音符 2:1比例")

def _4_4_funk_sixteenth() -> RhythmPattern:
    """放克十六分音符"""
    vels = [95, 55, 65, 55, 90, 55, 65, 55, 80, 55, 65, 55, 90, 55, 70, 55]
    events = [NoteEvent(None, 0.25, v) for v in vels]
    return RhythmPattern("4/4 Funk Sixteenth", TimeSignature.FOUR_FOUR, events, 100,
                         "放克十六分音符切分节奏")

def _4_4_hiphop() -> RhythmPattern:
    """Hip-Hop节拍：重底鼓+军鼓backbeat"""
    events = [
        NoteEvent(None, 0.5, 100),    # 底鼓 (beat 1 前半)
        NoteEvent(None, 0.5, 45),     # 踩镲 (beat 1 后半)
        NoteEvent(None, 0.5, 90),     # 军鼓 (beat 2 前半 backbeat)
        NoteEvent(None, 0.5, 45),     # 踩镲 (beat 2 后半)
        NoteEvent(None, 0.5, 95),     # 底鼓 (beat 3 前半)
        NoteEvent(None, 0.5, 45),     # 踩镲 (beat 3 后半)
        NoteEvent(None, 0.5, 90),     # 军鼓 (beat 4 前半 backbeat)
        NoteEvent(None, 0.5, 45),     # 踩镲 (beat 4 后半)
    ]
    return RhythmPattern("4/4 Hip-Hop", TimeSignature.FOUR_FOUR, events, 90,
                         "Hip-Hop节拍：重底鼓+军鼓backbeat")

def _4_4_reggae() -> RhythmPattern:
    """雷鬼节奏：反拍重音"""
    events = [
        NoteEvent(None, 0.5, 50),     # 弱
        NoteEvent(None, 0.5, 100),    # 强（反拍）
        NoteEvent(None, 0.5, 50),     # 弱
        NoteEvent(None, 0.5, 95),     # 强（反拍）
        NoteEvent(None, 0.5, 50),     # 弱
        NoteEvent(None, 0.5, 100),    # 强（反拍）
        NoteEvent(None, 0.5, 50),     # 弱
        NoteEvent(None, 0.5, 95),     # 强（反拍）
    ]
    return RhythmPattern("4/4 Reggae", TimeSignature.FOUR_FOUR, events, 80,
                         "雷鬼节奏：反拍重音（skank）")

def _4_4_disco() -> RhythmPattern:
    """迪斯科：四四拍four-on-the-floor"""
    events = [
        NoteEvent(None, 0.5, 100),    # 底鼓
        NoteEvent(None, 0.5, 60),     # 踩镲
    ] * 4
    return RhythmPattern("4/4 Disco (Four-on-floor)", TimeSignature.FOUR_FOUR, events, 120,
                         "迪斯科节奏：每拍底鼓+踩镲")

def _4_4_ballad() -> RhythmPattern:
    """抒情歌曲：慢速宽广"""
    events = [
        NoteEvent(None, 2.0, 80, dotted=True),   # 附点二分音符 (3 beats)
        NoteEvent(None, 1.0, 70),                 # 四分音符 (1 beat)
    ]
    return RhythmPattern("4/4 Ballad", TimeSignature.FOUR_FOUR, events, 70,
                         "抒情歌曲节奏：慢速宽广")

def _4_4_metal() -> RhythmPattern:
    """金属：双踩十六分音符"""
    vels = [100, 90, 100, 90, 85, 90, 100, 90, 100, 90, 100, 90, 85, 90, 100, 90]
    events = [NoteEvent(None, 0.25, v) for v in vels]
    return RhythmPattern("4/4 Metal Gallop", TimeSignature.FOUR_FOUR, events, 160,
                         "金属节奏：密集十六分音符gallop")

def _4_4_synth_pop() -> RhythmPattern:
    """合成器流行：电子八分+十六分混合"""
    events = [
        NoteEvent(None, 0.5, 85),
        NoteEvent(None, 0.25, 60),
        NoteEvent(None, 0.25, 70),
        NoteEvent(None, 0.5, 80),
        NoteEvent(None, 0.5, 85),
        NoteEvent(None, 0.25, 60),
        NoteEvent(None, 0.25, 70),
        NoteEvent(None, 0.5, 80),
        NoteEvent(None, 0.5, 75),
        NoteEvent(None, 0.5, 75),
    ]
    return RhythmPattern("4/4 Synth Pop", TimeSignature.FOUR_FOUR, events, 128,
                         "合成器流行：电子节拍混合八分十六分")

def _4_4_blues_shuffle() -> RhythmPattern:
    """布鲁斯 Shuffle：三连音感"""
    events = [
        NoteEvent(None, 0.67, 90),
        NoteEvent(None, 0.33, 55),
        NoteEvent(None, 0.67, 75),
        NoteEvent(None, 0.33, 55),
        NoteEvent(None, 0.67, 85),
        NoteEvent(None, 0.33, 55),
        NoteEvent(None, 0.67, 75),
        NoteEvent(None, 0.33, 55),
    ]
    return RhythmPattern("4/4 Blues Shuffle", TimeSignature.FOUR_FOUR, events, 90,
                         "布鲁斯Shuffle：triplet feel八分音符")

def _4_4_country() -> RhythmPattern:
    """乡村音乐：boom-chick"""
    events = [
        NoteEvent(None, 0.5, 95),    # bass (boom)
        NoteEvent(None, 0.5, 70),    # chord (chick)
        NoteEvent(None, 0.5, 90),    # bass
        NoteEvent(None, 0.5, 70),    # chord
        NoteEvent(None, 0.5, 95),    # bass
        NoteEvent(None, 0.5, 70),    # chord
        NoteEvent(None, 0.5, 90),    # bass
        NoteEvent(None, 0.5, 70),    # chord
    ]
    return RhythmPattern("4/4 Country (Boom-Chick)", TimeSignature.FOUR_FOUR, events, 110,
                         "乡村音乐：boom-chick交替低音")


# ============================================================
# 3/4 拍模式库
# ============================================================

def _3_4_waltz_classic() -> RhythmPattern:
    """古典华尔兹：强-弱-弱"""
    events = [
        NoteEvent(None, 1.0, 100),
        NoteEvent(None, 1.0, 55),
        NoteEvent(None, 1.0, 55),
    ]
    return RhythmPattern("3/4 Classic Waltz", TimeSignature.THREE_FOUR, events, 100,
                         "古典华尔兹：强-弱-弱")

def _3_4_jazz_waltz() -> RhythmPattern:
    """爵士华尔兹：swing 3/4"""
    events = [
        NoteEvent(None, 0.67, 90),
        NoteEvent(None, 0.33, 50),
        NoteEvent(None, 0.67, 75),
        NoteEvent(None, 0.33, 50),
        NoteEvent(None, 0.67, 80),
        NoteEvent(None, 0.33, 50),
    ]
    return RhythmPattern("3/4 Jazz Waltz", TimeSignature.THREE_FOUR, events, 130,
                         "爵士华尔兹：swing feel 3/4")

def _3_4_ballad_slow() -> RhythmPattern:
    """慢速3/4抒情"""
    events = [
        NoteEvent(None, 1.5, 80, dotted=True),
        NoteEvent(None, 1.5, 65, dotted=True),
    ]
    return RhythmPattern("3/4 Slow Ballad", TimeSignature.THREE_FOUR, events, 65,
                         "慢速3/4抒情：附点节奏")

def _3_4_folk() -> RhythmPattern:
    """民谣3/4"""
    events = [
        NoteEvent(None, 0.5, 90),
        NoteEvent(None, 0.5, 60),
        NoteEvent(None, 1.0, 70),
        NoteEvent(None, 0.5, 85),
        NoteEvent(None, 0.5, 60),
        NoteEvent(None, 1.0, 65),
    ]
    return RhythmPattern("3/4 Folk", TimeSignature.THREE_FOUR, events, 95,
                         "民谣3/4：自然流露的律动")

def _3_4_mazurka() -> RhythmPattern:
    """玛祖卡：第二三拍重音"""
    events = [
        NoteEvent(None, 1.0, 60),
        NoteEvent(None, 1.0, 100),
        NoteEvent(None, 1.0, 90),
    ]
    return RhythmPattern("3/4 Mazurka", TimeSignature.THREE_FOUR, events, 120,
                         "玛祖卡：第二或第三拍重音")


# ============================================================
# 2/4 拍模式库
# ============================================================

def _2_4_march() -> RhythmPattern:
    """进行曲：强-弱"""
    events = [
        NoteEvent(None, 1.0, 100),
        NoteEvent(None, 1.0, 55),
    ]
    return RhythmPattern("2/4 March", TimeSignature.TWO_FOUR, events, 120,
                         "进行曲节奏：强-弱交替")

def _2_4_polka() -> RhythmPattern:
    """波尔卡：跳跃八分音符"""
    events = [
        NoteEvent(None, 0.5, 90),
        NoteEvent(None, 0.5, 70),
        NoteEvent(None, 0.5, 85),
        NoteEvent(None, 0.5, 65),
    ]
    return RhythmPattern("2/4 Polka", TimeSignature.TWO_FOUR, events, 140,
                         "波尔卡：跳跃八分音符")

def _2_4_samba() -> RhythmPattern:
    """桑巴2/4"""
    events = [
        NoteEvent(None, 0.5, 95),
        NoteEvent(None, 0.25, 60),
        NoteEvent(None, 0.25, 70),
        NoteEvent(None, 0.5, 90),
        NoteEvent(None, 0.5, 75),
    ]
    return RhythmPattern("2/4 Samba", TimeSignature.TWO_FOUR, events, 100,
                         "桑巴节奏：巴西律动")

def _2_4_bluegrass() -> RhythmPattern:
    """蓝草音乐"""
    events = [
        NoteEvent(None, 0.5, 90),
        NoteEvent(None, 0.25, 60),
        NoteEvent(None, 0.25, 60),
        NoteEvent(None, 0.5, 80),
        NoteEvent(None, 0.5, 65),
    ]
    return RhythmPattern("2/4 Bluegrass", TimeSignature.TWO_FOUR, events, 130,
                         "蓝草音乐：快速跳跃节奏")


# ============================================================
# 6/8 拍模式库（复合拍）
# ============================================================

def _6_8_jig() -> RhythmPattern:
    """吉格舞曲：两组三连音"""
    events = [
        NoteEvent(None, 0.5, 100),
        NoteEvent(None, 0.5, 55),
        NoteEvent(None, 0.5, 60),
        NoteEvent(None, 0.5, 90),
        NoteEvent(None, 0.5, 55),
        NoteEvent(None, 0.5, 60),
    ]
    return RhythmPattern("6/8 Jig", TimeSignature.SIX_EIGHT, events, 120,
                         "爱尔兰吉格舞曲：两组三连音")

def _6_8_ballad() -> RhythmPattern:
    """6/8抒情：缓慢摇摆"""
    events = [
        NoteEvent(None, 1.5, 85),
        NoteEvent(None, 1.5, 65),
        NoteEvent(None, 0.75, 55),
        NoteEvent(None, 0.75, 50),
        NoteEvent(None, 1.5, 70),
    ]
    return RhythmPattern("6/8 Slow Ballad", TimeSignature.SIX_EIGHT, events, 60,
                         "6/8抒情：缓慢摇摆感觉")

def _6_8_rock() -> RhythmPattern:
    """6/8摇滚"""
    events = [
        NoteEvent(None, 0.5, 100),
        NoteEvent(None, 0.5, 50),
        NoteEvent(None, 0.5, 70),
        NoteEvent(None, 0.5, 95),
        NoteEvent(None, 0.5, 50),
        NoteEvent(None, 0.5, 70),
    ]
    return RhythmPattern("6/8 Rock", TimeSignature.SIX_EIGHT, events, 90,
                         "6/8摇滚：两组三连音律动")

def _6_8_african() -> RhythmPattern:
    """非洲风格6/8"""
    vels = [100, 55, 75, 60, 90, 70]
    events = [NoteEvent(None, 0.5, v) for v in vels]
    return RhythmPattern("6/8 African", TimeSignature.SIX_EIGHT, events, 110,
                         "非洲风格6/8：交叉节奏基础")

def _6_8_swing_slow() -> RhythmPattern:
    """慢速swing 6/8"""
    events = [
        NoteEvent(None, 1.0, 90, dotted=True),
        NoteEvent(None, 0.5, 55),
        NoteEvent(None, 1.0, 75, dotted=True),
        NoteEvent(None, 0.5, 55),
        NoteEvent(None, 1.0, 80, dotted=True),
        NoteEvent(None, 0.5, 50),
    ]
    return RhythmPattern("6/8 Slow Swing", TimeSignature.SIX_EIGHT, events, 70,
                         "慢速swing 6/8：慵懒律动")


# ============================================================
# 12/8 拍模式库
# ============================================================

def _12_8_slow_blues() -> RhythmPattern:
    """12/8慢速蓝调"""
    vels = [100, 50, 60, 50, 85, 50, 60, 50, 90, 50, 60, 50]
    events = [NoteEvent(None, 0.5, v) for v in vels]
    return RhythmPattern("12/8 Slow Blues", TimeSignature.TWELVE_EIGHT, events, 60,
                         "12/8慢速蓝调：Shuffle feel")

def _12_8_gospel() -> RhythmPattern:
    """12/8福音音乐"""
    vels = [95, 55, 70, 85, 55, 70, 90, 55, 70, 85, 55, 75]
    events = [NoteEvent(None, 0.5, v) for v in vels]
    return RhythmPattern("12/8 Gospel", TimeSignature.TWELVE_EIGHT, events, 75,
                         "12/8福音音乐：swing triplet feel")


# ============================================================
# 5/4 拍模式库（不对称拍号）
# ============================================================

def _5_4_jazz() -> RhythmPattern:
    """5/4爵士（Take Five风格）：3+2分组"""
    from .rhythm import TimeSignature as TS
    # 自定义拍号不使用enum，用4/4容器但标注5/4
    events = [
        NoteEvent(None, 1.0, 100),
        NoteEvent(None, 1.0, 55),
        NoteEvent(None, 1.0, 70),
        NoteEvent(None, 0.5, 85),
        NoteEvent(None, 0.5, 60),
        NoteEvent(None, 1.0, 75),
    ]
    # 由于TimeSignature enum没有5/4，用FOUR_FOUR作载体但实际是5/4
    return RhythmPattern("5/4 Jazz (Take Five)", TimeSignature.FOUR_FOUR, events, 160,
                         "5/4爵士：3+2分组，Take Five风格")

def _5_4_progressive() -> RhythmPattern:
    """5/4前卫摇滚：2+3分组"""
    events = [
        NoteEvent(None, 0.5, 100),
        NoteEvent(None, 0.5, 55),
        NoteEvent(None, 1.0, 85),
        NoteEvent(None, 0.5, 60),
        NoteEvent(None, 0.5, 70),
        NoteEvent(None, 0.5, 90),
        NoteEvent(None, 0.5, 55),
        NoteEvent(None, 1.0, 75),
    ]
    return RhythmPattern("5/4 Progressive", TimeSignature.FOUR_FOUR, events, 140,
                         "5/4前卫摇滚：2+3分组")


# ============================================================
# 7/8 拍模式库（巴尔干/不对称）
# ============================================================

def _7_8_balkan() -> RhythmPattern:
    """巴尔干7/8：2+2+3分组"""
    events = [
        NoteEvent(None, 0.5, 100),
        NoteEvent(None, 0.5, 55),
        NoteEvent(None, 0.5, 90),
        NoteEvent(None, 0.5, 50),
        NoteEvent(None, 0.5, 85),
        NoteEvent(None, 0.25, 60),
        NoteEvent(None, 0.25, 70),
    ]
    return RhythmPattern("7/8 Balkan", TimeSignature.FOUR_FOUR, events, 130,
                         "巴尔干7/8：2+2+3分组快速舞曲")

def _7_8_progressive() -> RhythmPattern:
    """前卫7/8：3+2+2分组"""
    events = [
        NoteEvent(None, 0.5, 95),
        NoteEvent(None, 0.25, 55),
        NoteEvent(None, 0.25, 65),
        NoteEvent(None, 0.5, 85),
        NoteEvent(None, 0.5, 50),
        NoteEvent(None, 0.5, 90),
        NoteEvent(None, 0.5, 55),
        NoteEvent(None, 0.5, 70),
    ]
    return RhythmPattern("7/8 Progressive", TimeSignature.FOUR_FOUR, events, 120,
                         "前卫7/8：3+2+2分组")


# ============================================================
# 节奏模式注册表
# ============================================================

# 所有模式生成函数的注册表
_PATTERN_BUILDERS: Dict[str, Callable[[], RhythmPattern]] = {
    # 4/4
    "4/4_basic_pop":       _4_4_basic_pop,
    "4/4_eighth_pop":      _4_4_eighth_pop,
    "4/4_rock_steady":     _4_4_rock_steady,
    "4/4_jazz_swing":      _4_4_jazz_swing,
    "4/4_funk_sixteenth":  _4_4_funk_sixteenth,
    "4/4_hiphop":          _4_4_hiphop,
    "4/4_reggae":          _4_4_reggae,
    "4/4_disco":           _4_4_disco,
    "4/4_ballad":          _4_4_ballad,
    "4/4_metal":           _4_4_metal,
    "4/4_synth_pop":       _4_4_synth_pop,
    "4/4_blues_shuffle":   _4_4_blues_shuffle,
    "4/4_country":         _4_4_country,
    # 3/4
    "3/4_waltz":           _3_4_waltz_classic,
    "3/4_jazz_waltz":      _3_4_jazz_waltz,
    "3/4_ballad":          _3_4_ballad_slow,
    "3/4_folk":            _3_4_folk,
    "3/4_mazurka":         _3_4_mazurka,
    # 2/4
    "2/4_march":           _2_4_march,
    "2/4_polka":           _2_4_polka,
    "2/4_samba":           _2_4_samba,
    "2/4_bluegrass":       _2_4_bluegrass,
    # 6/8
    "6/8_jig":             _6_8_jig,
    "6/8_ballad":          _6_8_ballad,
    "6/8_rock":            _6_8_rock,
    "6/8_african":         _6_8_african,
    "6/8_swing_slow":      _6_8_swing_slow,
    # 12/8
    "12/8_slow_blues":     _12_8_slow_blues,
    "12/8_gospel":         _12_8_gospel,
    # 5/4
    "5/4_jazz":            _5_4_jazz,
    "5/4_progressive":     _5_4_progressive,
    # 7/8
    "7/8_balkan":          _7_8_balkan,
    "7/8_progressive":     _7_8_progressive,
}


# 按拍号分组的索引
PATTERNS_BY_METER: Dict[str, List[str]] = {
    "4/4": [k for k in _PATTERN_BUILDERS if k.startswith("4/4")],
    "3/4": [k for k in _PATTERN_BUILDERS if k.startswith("3/4")],
    "2/4": [k for k in _PATTERN_BUILDERS if k.startswith("2/4")],
    "6/8": [k for k in _PATTERN_BUILDERS if k.startswith("6/8")],
    "12/8": [k for k in _PATTERN_BUILDERS if k.startswith("12/8")],
    "5/4": [k for k in _PATTERN_BUILDERS if k.startswith("5/4")],
    "7/8": [k for k in _PATTERN_BUILDERS if k.startswith("7/8")],
}

# 按风格分组（多对一映射）
STYLE_GROUPS: Dict[str, List[str]] = {
    "Pop":        ["4/4_basic_pop", "4/4_eighth_pop", "4/4_synth_pop"],
    "Rock":       ["4/4_rock_steady", "4/4_metal", "6/8_rock"],
    "Jazz":       ["4/4_jazz_swing", "3/4_jazz_waltz", "5/4_jazz", "6/8_swing_slow"],
    "Funk":       ["4/4_funk_sixteenth", "4/4_disco"],
    "Hip-Hop":    ["4/4_hiphop"],
    "Latin":      ["2/4_samba"],
    "Reggae":     ["4/4_reggae"],
    "Blues":      ["4/4_blues_shuffle", "12/8_slow_blues"],
    "Folk":       ["3/4_folk", "2/4_bluegrass", "6/8_jig"],
    "Country":    ["4/4_country"],
    "Ballad":     ["4/4_ballad", "3/4_ballad", "6/8_ballad"],
    "Classical":  ["3/4_waltz", "3/4_mazurka", "2/4_march", "2/4_polka"],
    "Progressive": ["5/4_progressive", "7/8_progressive", "7/8_balkan"],
    "Gospel":     ["12/8_gospel"],
    "World":      ["6/8_african", "7/8_balkan"],
}


class RhythmLibrary:
    """
    节奏模式库 - 统一入口
    
    用法:
        lib = RhythmLibrary()
        pattern = lib.get("4/4_rock_steady")
        jazz_patterns = lib.by_style("Jazz")
        all_4_4 = lib.by_meter("4/4")
    """

    def __init__(self):
        self._cache: Dict[str, RhythmPattern] = {}

    def get(self, pattern_id: str) -> RhythmPattern:
        """获取指定节奏模式（延迟构建+缓存）"""
        if pattern_id not in _PATTERN_BUILDERS:
            raise KeyError(f"未知节奏模式: {pattern_id}。可用: {list(_PATTERN_BUILDERS.keys())}")
        if pattern_id not in self._cache:
            self._cache[pattern_id] = _PATTERN_BUILDERS[pattern_id]()
        return self._cache[pattern_id]

    def by_meter(self, meter: str) -> List[RhythmPattern]:
        """按拍号获取所有模式"""
        keys = PATTERNS_BY_METER.get(meter, [])
        return [self.get(k) for k in keys]

    def by_style(self, style: str) -> List[RhythmPattern]:
        """按风格获取所有模式"""
        keys = STYLE_GROUPS.get(style, [])
        return [self.get(k) for k in keys]

    def all_patterns(self) -> Dict[str, RhythmPattern]:
        """获取所有模式"""
        return {k: self.get(k) for k in _PATTERN_BUILDERS}

    def list_meters(self) -> List[str]:
        """列出所有拍号"""
        return list(PATTERNS_BY_METER.keys())

    def list_styles(self) -> List[str]:
        """列出所有风格"""
        return list(STYLE_GROUPS.keys())

    def search(self, keyword: str) -> List[RhythmPattern]:
        """按关键词搜索模式（匹配名称或描述）"""
        keyword = keyword.lower()
        results = []
        for pid, builder in _PATTERN_BUILDERS.items():
            pattern = self.get(pid)
            if keyword in pattern.name.lower() or keyword in pattern.description.lower():
                results.append(pattern)
        return results

    def random(self, meter: Optional[str] = None, style: Optional[str] = None) -> RhythmPattern:
        """随机获取一个模式"""
        import random
        if meter:
            pool = PATTERNS_BY_METER.get(meter, list(_PATTERN_BUILDERS.keys()))
        elif style:
            pool = STYLE_GROUPS.get(style, list(_PATTERN_BUILDERS.keys()))
        else:
            pool = list(_PATTERN_BUILDERS.keys())
        return self.get(random.choice(pool))

    def count(self) -> int:
        """模式总数"""
        return len(_PATTERN_BUILDERS)

    def summary(self) -> Dict[str, int]:
        """按拍号统计模式数量"""
        return {meter: len(keys) for meter, keys in PATTERNS_BY_METER.items()}
