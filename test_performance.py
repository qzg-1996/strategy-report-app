#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
性能测试脚本 - 验证优化效果
"""
import time
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.strategy_manager import StrategyManager

def test_summary_performance():
    """测试策略汇总性能"""
    print("=" * 50)
    print("策略汇总性能测试")
    print("=" * 50)
    
    manager = StrategyManager()
    
    start = time.time()
    data = manager.get_summary_data()
    end = time.time()
    
    print(f"策略数量: {len(data.get('strategies', []))}")
    print(f"总持仓: {data.get('total_position', 0)} 吨")
    print(f"执行时间: {end - start:.2f} 秒")
    
    if end - start > 5:
        print("⚠️ 警告: 执行时间超过5秒，仍需优化")
    else:
        print("✓ 性能良好")
    
    return end - start

def test_weekly_data_performance():
    """测试复盘数据性能"""
    print("\n" + "=" * 50)
    print("复盘数据性能测试")
    print("=" * 50)
    
    manager = StrategyManager()
    
    # 获取策略列表
    import sqlite3
    conn = sqlite3.connect(manager.db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM strategies ORDER BY sort_order, id')
    columns = [description[0] for description in cursor.description]
    strategies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    
    if not strategies:
        print("没有策略数据，跳过测试")
        return 0
    
    print(f"策略数量: {len(strategies)}")
    
    # 测试批量获取
    start = time.time()
    all_data = manager.get_all_strategies_weekly_data(strategies)
    end = time.time()
    
    print(f"批量获取执行时间: {end - start:.2f} 秒")
    
    if end - start > 5:
        print("⚠️ 警告: 执行时间超过5秒")
    else:
        print("✓ 性能良好")
    
    return end - start

if __name__ == '__main__':
    try:
        t1 = test_summary_performance()
        t2 = test_weekly_data_performance()
        
        print("\n" + "=" * 50)
        print("测试完成!")
        print(f"总耗时: {t1 + t2:.2f} 秒")
        print("=" * 50)
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
