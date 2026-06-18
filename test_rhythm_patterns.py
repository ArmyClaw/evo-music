#!/usr/bin/env python3
"""
节奏模式库测试 - 验证所有节奏pattern的正确性
覆盖: 4/4, 3/4, 2/4, 6/8, 12/8, 5/4, 7/8
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evo_music.rhythm_patterns import (
    RhythmLibrary, PATTERNS_BY_METER, STYLE_GROUPS,
    _PATTERN_BUILDERS,
)
from evo_music.rhythm import RhythmPattern, RhythmAnalyzer, TimeSignature


def test_library_completeness():
    """测试模式库完整性"""
    print("=== 节奏模式库完整性测试 ===")
    lib = RhythmLibrary()

    # 1. 检查总模式数
    total = lib.count()
    print(f"\n总模式数: {total}")
    assert total >= 30, f"模式太少({total})，应至少30个"

    # 2. 检查拍号覆盖
    meters = lib.list_meters()
    print(f"拍号覆盖: {meters}")
    for expected in ["4/4", "3/4", "2/4", "6/8", "12/8", "5/4", "7/8"]:
        assert expected in meters, f"缺少拍号 {expected}"

    # 3. 检查每个拍号都有模式
    summary = lib.summary()
    print(f"拍号分布: {summary}")
    for meter, count in summary.items():
        assert count > 0, f"拍号 {meter} 没有任何模式"

    # 4. 检查风格覆盖
    styles = lib.list_styles()
    print(f"风格覆盖: {styles}")
    for expected_style in ["Pop", "Rock", "Jazz", "Funk", "Hip-Hop", "Blues", "Ballad"]:
        assert expected_style in styles, f"缺少风格 {expected_style}"

    print("✅ 完整性测试通过")


def test_all_patterns_valid():
    """验证每个模式的数据有效性"""
    print("\n=== 模式数据有效性测试 ===")
    lib = RhythmLibrary()
    all_patterns = lib.all_patterns()

    for pid, pattern in all_patterns.items():
        # 名称非空
        assert pattern.name, f"{pid}: 名称为空"
        # 有拍号
        assert pattern.time_signature is not None, f"{pid}: 拍号为空"
        # 至少有一个事件
        assert len(pattern.note_events) > 0, f"{pid}: 没有音符事件"
        # 总拍数 > 0
        beats = pattern.get_total_beats()
        assert beats > 0, f"{pid}: 总拍数为0"
        # BPM 合理
        assert 40 <= pattern.bpm <= 250, f"{pid}: BPM={pattern.bpm} 超出范围"
        # 描述非空
        assert pattern.description, f"{pid}: 描述为空"
        # 每个事件力度在合理范围
        for ev in pattern.note_events:
            assert 0 <= ev.velocity <= 127, f"{pid}: 力度={ev.velocity} 超出MIDI范围"
            assert ev.duration > 0, f"{pid}: 存在时长为0的事件"

    print(f"✅ 全部 {len(all_patterns)} 个模式数据有效")


def test_4_4_patterns():
    """测试4/4拍模式（应有最丰富的模式）"""
    print("\n=== 4/4拍模式测试 ===")
    lib = RhythmLibrary()
    patterns_4_4 = lib.by_meter("4/4")
    print(f"4/4模式数: {len(patterns_4_4)}")
    assert len(patterns_4_4) >= 10, "4/4拍应至少有10个模式"

    # 验证每个模式总拍数接近4的倍数（允许小误差）
    for p in patterns_4_4:
        beats = p.get_total_beats()
        remainder = beats % 4
        assert remainder < 0.15 or remainder > 3.85, \
            f"{p.name}: 总拍数={beats:.2f}，不是4的整数倍"

    print("✅ 4/4拍模式测试通过")


def test_compound_meter():
    """测试复合拍号（6/8, 12/8）"""
    print("\n=== 复合拍号测试 ===")
    lib = RhythmLibrary()

    # 6/8
    patterns_6_8 = lib.by_meter("6/8")
    print(f"6/8模式数: {len(patterns_6_8)}")
    assert len(patterns_6_8) >= 3, "6/8拍应至少有3个模式"
    for p in patterns_6_8:
        beats = p.get_total_beats()
        # 6/8拍一小节 = 3拍（以四分音符计）或6个八分音符
        assert beats > 0, f"{p.name}: 总拍数应为正数"

    # 12/8
    patterns_12_8 = lib.by_meter("12/8")
    print(f"12/8模式数: {len(patterns_12_8)}")
    assert len(patterns_12_8) >= 2, "12/8拍应至少有2个模式"

    print("✅ 复合拍号测试通过")


def test_style_groups():
    """测试风格分组"""
    print("\n=== 风格分组测试 ===")
    lib = RhythmLibrary()

    for style, pattern_ids in STYLE_GROUPS.items():
        assert len(pattern_ids) > 0, f"风格 {style} 没有模式"
        patterns = lib.by_style(style)
        print(f"  {style}: {len(patterns)}个模式")
        assert len(patterns) == len(pattern_ids), \
            f"风格 {style}: 期望{len(pattern_ids)}个，实际{len(patterns)}个"

    print("✅ 风格分组测试通过")


def test_search():
    """测试搜索功能"""
    print("\n=== 搜索功能测试 ===")
    lib = RhythmLibrary()

    results = lib.search("blues")
    print(f"搜索 'blues': 找到 {len(results)} 个")
    assert len(results) >= 2, "搜索blues应至少找到2个结果"

    results = lib.search("jazz")
    print(f"搜索 'jazz': 找到 {len(results)} 个")
    assert len(results) >= 2, "搜索jazz应至少找到2个结果"

    results = lib.search("rock")
    print(f"搜索 'rock': 找到 {len(results)} 个")
    assert len(results) >= 1, "搜索rock应至少找到1个结果"

    print("✅ 搜索功能测试通过")


def test_repeat_and_combine():
    """测试模式重复和组合"""
    print("\n=== 模式重复测试 ===")
    lib = RhythmLibrary()
    pattern = lib.get("4/4_basic_pop")

    # 重复4次
    repeated = pattern.repeat(4)
    expected_beats = pattern.get_total_beats() * 4
    actual_beats = repeated.get_total_beats()
    print(f"原模式拍数: {pattern.get_total_beats()}, 重复4次后: {actual_beats}")
    assert abs(actual_beats - expected_beats) < 0.01, "重复后拍数不一致"

    print("✅ 模式重复测试通过")


def test_analysis():
    """测试节奏分析器对库中模式的分析"""
    print("\n=== 节奏分析测试 ===")
    lib = RhythmLibrary()
    analyzer = RhythmAnalyzer()

    for pid in list(_PATTERN_BUILDERS.keys())[:8]:  # 抽样分析前8个
        pattern = lib.get(pid)
        analysis = analyzer.analyze_pattern(pattern)
        print(f"  {pattern.name}: 密度={analysis['rhythmic_density']:.2f}, "
              f"复杂度={analysis['complexity']}, 切分={analysis['syncopation']:.0f}%")
        assert analysis["total_beats"] > 0
        assert analysis["complexity"] in ["Simple", "Medium", "Complex"]

    print("✅ 节奏分析测试通过")


def test_random():
    """测试随机获取"""
    print("\n=== 随机获取测试 ===")
    lib = RhythmLibrary()

    p = lib.random()
    assert p is not None
    print(f"随机模式: {p.name}")

    p = lib.random(meter="3/4")
    assert "3/4" in p.name
    print(f"3/4随机模式: {p.name}")

    p = lib.random(style="Jazz")
    print(f"Jazz随机模式: {p.name}")

    print("✅ 随机获取测试通过")


def test_to_dict():
    """测试序列化"""
    print("\n=== 序列化测试 ===")
    lib = RhythmLibrary()
    pattern = lib.get("4/4_rock_steady")
    d = pattern.to_dict()

    assert "name" in d
    assert "time_signature" in d
    assert "note_events" in d
    assert "bpm" in d
    assert len(d["note_events"]) > 0
    print(f"模式 {d['name']} 序列化: {len(d['note_events'])} 事件, "
          f"拍号={d['time_signature']}, BPM={d['bpm']}")

    print("✅ 序列化测试通过")


if __name__ == "__main__":
    try:
        test_library_completeness()
        test_all_patterns_valid()
        test_4_4_patterns()
        test_compound_meter()
        test_style_groups()
        test_search()
        test_repeat_and_combine()
        test_analysis()
        test_random()
        test_to_dict()

        print("\n" + "=" * 50)
        print("🎉 所有测试通过！节奏模式库实现成功。")
        print("=" * 50)

        # 打印总结
        lib = RhythmLibrary()
        print(f"\n📊 节奏模式库总结:")
        print(f"  总模式数: {lib.count()}")
        print(f"  拍号分布:")
        for meter, count in lib.summary().items():
            print(f"    {meter}: {count}个")
        print(f"  风格分布:")
        for style, count in [(s, len(ids)) for s, ids in STYLE_GROUPS.items()]:
            print(f"    {style}: {count}个")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
