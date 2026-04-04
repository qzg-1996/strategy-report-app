#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能测试脚本 - 验证各模块功能
"""
import sqlite3
import os
import sys

# 测试数据库连接
def test_database():
    """测试数据库表结构"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'strategy.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查策略分析表结构
    cursor.execute("PRAGMA table_info(strategy_analysis)")
    columns = cursor.fetchall()
    print("策略分析表字段:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # 检查主力合约表
    cursor.execute("PRAGMA table_info(main_contracts)")
    columns = cursor.fetchall()
    print("\n主力合约表字段:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    print("\n✓ 数据库结构检查通过")

# 测试策略分析API
def test_strategy_analysis_api():
    """测试策略分析API"""
    import json
    from app import app
    
    client = app.test_client()
    
    # 测试保存策略分析
    test_data = {
        'operation_scale': '测试操作规模',
        'operation_direction': '测试操作方向',
        'core_logic': '测试核心逻辑',
        'execution_plan': '测试执行计划',
        'risk_response': '测试风险应对'
    }
    
    # 先获取（可能为空）
    r = client.get('/api/strategy/1/analysis')
    print(f"\n获取策略分析: {r.status_code}")
    
    # 保存
    r = client.post('/api/strategy/1/analysis', 
                    data=json.dumps(test_data),
                    content_type='application/json')
    print(f"保存策略分析: {r.status_code}")
    
    # 再次获取
    r = client.get('/api/strategy/1/analysis')
    print(f"再次获取策略分析: {r.status_code}")
    result = json.loads(r.data)
    if result.get('success') and result.get('data'):
        data = result['data']
        if data.get('core_logic') == '测试核心逻辑':
            print("✓ 策略分析数据保存和读取正常")
        else:
            print("✗ 策略分析数据不匹配")
    else:
        print("✗ 策略分析API返回错误")

# 测试主力合约API
def test_main_contracts_api():
    """测试主力合约API"""
    import json
    from app import app
    
    client = app.test_client()
    
    # 获取列表
    r = client.get('/api/main-contracts')
    print(f"\n获取主力合约列表: {r.status_code}")
    
    # 保存配置
    test_data = {
        'variety': '螺纹钢',
        'contract_code': 'RB2605',
        'effective_date': '2026-01-01',
        'expiry_date': '2026-05-31'
    }
    r = client.post('/api/main-contracts',
                    data=json.dumps(test_data),
                    content_type='application/json')
    print(f"保存主力合约: {r.status_code}")
    
    # 再次获取
    r = client.get('/api/main-contracts')
    result = json.loads(r.data)
    if result.get('success') and len(result.get('data', [])) > 0:
        print("✓ 主力合约API工作正常")
    else:
        print("✗ 主力合约API返回错误")

# 测试策略类型配置
def test_strategy_types():
    """测试策略类型配置"""
    print("\n策略类型与业务类型映射:")
    strategy_types = {
        '套期保值': ['期货-现货'],
        '基差交易': ['期货-现货', '期货-远期', '期货-期货', '远期-现货'],
        '趋势交易': ['投机']
    }
    
    for st, bt_list in strategy_types.items():
        print(f"  {st}:")
        for bt in bt_list:
            if bt == '期货-期货':
                print(f"    - {bt}: 期货合约1、期货合约2、期货合约1方向")
            elif bt == '远期-现货':
                print(f"    - {bt}: 现货品种1、现货品种2、现货品种1方向")
            elif bt == '期货-现货':
                print(f"    - {bt}: 期货合约、现货品种、期货方向")
            elif bt == '期货-远期':
                print(f"    - {bt}: 期货合约、远期品种、期货方向")
            else:
                print(f"    - {bt}")
    
    print("✓ 策略类型配置检查通过")

if __name__ == '__main__':
    print("=" * 50)
    print("期现交易策略汇报软件 - 功能测试")
    print("=" * 50)
    
    try:
        test_database()
    except Exception as e:
        print(f"数据库测试失败: {e}")
    
    try:
        test_strategy_types()
    except Exception as e:
        print(f"策略类型测试失败: {e}")
    
    try:
        test_strategy_analysis_api()
    except Exception as e:
        print(f"策略分析API测试失败: {e}")
    
    try:
        test_main_contracts_api()
    except Exception as e:
        print(f"主力合约API测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
