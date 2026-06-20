#!/usr/bin/env python3
"""
最简单的和声编排测试
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def test_basic_import():
    """测试基本导入"""
    try:
        from evo_music.harmony_arranger import HarmonyArranger, HarmonyConfig
        print("✅ 导入成功")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_config_creation():
    """测试配置创建"""
    try:
        from evo_music.harmony_arranger import HarmonyConfig
        config = HarmonyConfig()
        print("✅ 配置创建成功")
        return True
    except Exception as e:
        print(f"❌ 配置创建失败: {e}")
        return False

def test_arranger_creation():
    """测试和声编排器创建"""
    try:
        from evo_music.harmony_arranger import HarmonyArranger, HarmonyConfig
        config = HarmonyConfig()
        arranger = HarmonyArranger(config)
        print("✅ 和声编排器创建成功")
        return True
    except Exception as e:
        print(f"❌ 和声编排器创建失败: {e}")
        return False

def test_scale_creation():
    """测试调式创建"""
    try:
        from evo_music.scales import ScaleFactory, ScaleType
        from evo_music.notes import NoteName
        scale_factory = ScaleFactory()
        c_major = scale_factory.create_scale(NoteName.C, ScaleType.MAJOR)
        print("✅ 调式创建成功")
        return True
    except Exception as e:
        print(f"❌ 调式创建失败: {e}")
        return False

def test_minimal_harmony():
    """测试最小和声编排"""
    try:
        from evo_music.harmony_arranger import HarmonyArranger, HarmonyConfig
        from evo_music.scales import ScaleFactory, ScaleType
        
        # 创建配置
        config = HarmonyConfig()
        arranger = HarmonyArranger(config)
        
        # 创建调式
        from evo_music.notes import NoteName
        scale_factory = ScaleFactory()
        c_major = scale_factory.create_scale(NoteName.C, ScaleType.MAJOR)
        
        # 最小旋律
        melody_notes = [(60, 2), (64, 2), (67, 2), (60, 2)]
        
        # 生成和声
        result = arranger.arrange_harmony_for_melody(melody_notes, c_major)
        
        print("✅ 最小和声编排成功")
        return True
        
    except Exception as e:
        print(f"❌ 最小和声编排失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 逐步测试和声编排系统")
    print("=" * 40)
    
    tests = [
        test_basic_import,
        test_config_creation,
        test_arranger_creation,
        test_scale_creation,
        test_minimal_harmony
    ]
    
    for test in tests:
        print(f"\n🧪 执行测试: {test.__name__}")
        test()
    
    print("\n🏁 所有测试完成")