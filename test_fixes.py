# -*- coding: utf-8 -*-
"""
测试修复的功能
"""
import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:5000'

def test_get_strategies():
    """测试获取策略列表"""
    print("\n=== 测试获取策略列表 ===")
    try:
        resp = requests.get(f'{BASE_URL}/api/strategies', timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success'):
                strategies = data.get('data', [])
                print(f"✓ 成功获取 {len(strategies)} 个策略")
                if strategies:
                    print(f"  第一个策略: {strategies[0].get('strategy_code')} - {strategies[0].get('strategy_name')}")
                return True
            else:
                print(f"✗ 获取失败: {data.get('error')}")
                return False
        else:
            print(f"✗ HTTP错误: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_add_strategy():
    """测试添加策略"""
    print("\n=== 测试添加策略 ===")
    
    test_strategy = {
        'strategy_code': 'TEST-001',
        'strategy_name': '测试策略',
        'strategy_type': '基差交易',
        'business_type': '期货-现货',
        'futures_contract': 'RB2510',
        'futures_direction': '空',
        'spot_variety': '马钢螺纹',
        'plan_quantity': 1000
    }
    
    try:
        resp = requests.post(
            f'{BASE_URL}/api/strategies',
            json=test_strategy,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success'):
                print(f"✓ 添加策略成功: {test_strategy['strategy_code']}")
                return True
            else:
                print(f"✗ 添加失败: {data.get('error')}")
                return False
        else:
            print(f"✗ HTTP错误: {resp.status_code}")
            print(f"  响应: {resp.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_get_summary():
    """测试获取策略汇总"""
    print("\n=== 测试获取策略汇总 ===")
    try:
        resp = requests.get(f'{BASE_URL}/api/summary', timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success'):
                summary = data.get('data', {})
                strategies = summary.get('strategies', [])
                print(f"✓ 成功获取汇总数据")
                print(f"  策略数: {len(strategies)}")
                print(f"  总持仓: {summary.get('total_position')} 吨")
                print(f"  总持仓盈亏: {summary.get('total_position_profit')} 元")
                return True
            else:
                print(f"✗ 获取失败: {data.get('error')}")
                return False
        else:
            print(f"✗ HTTP错误: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_generate_report():
    """测试生成报告"""
    print("\n=== 测试生成报告 ===")
    
    # 首先获取策略列表
    try:
        resp = requests.get(f'{BASE_URL}/api/strategies', timeout=10)
        if resp.status_code != 200:
            print("✗ 无法获取策略列表")
            return False
        
        strategies_data = resp.json()
        if not strategies_data.get('success') or not strategies_data.get('data'):
            print("✗ 没有策略数据")
            return False
        
        strategies = strategies_data['data'][:2]  # 取前2个策略测试
        
        report_data = {
            'report_week': '2025-W13',
            'department': '测试部门',
            'price_trend': '测试价格走势',
            'production_status': '测试产量情况',
            'demand_status': '测试需求情况',
            'inventory_status': '测试库存情况',
            'macro_outlook': '测试宏观分析',
            'cost_outlook': '测试成本分析',
            'technical_outlook': '测试技术分析',
            'market_view': '测试市场观点',
            'rb_key_levels': '测试螺纹关键点位',
            'hc_key_levels': '测试热卷关键点位',
            'strategies': strategies
        }
        
        print(f"  使用 {len(strategies)} 个策略生成报告...")
        
        resp = requests.post(
            f'{BASE_URL}/api/generate-report',
            json=report_data,
            headers={'Content-Type': 'application/json'},
            timeout=120
        )
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success'):
                print(f"✓ 生成报告成功")
                print(f"  下载链接: {data.get('download_url')}")
                return True
            else:
                print(f"✗ 生成失败: {data.get('error')}")
                if 'traceback' in data:
                    print(f"  详细错误:\n{data['traceback'][:500]}")
                return False
        else:
            print(f"✗ HTTP错误: {resp.status_code}")
            print(f"  响应: {resp.text[:200]}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 50)
    print("测试期现交易策略汇报软件修复")
    print("=" * 50)
    print(f"\n服务器地址: {BASE_URL}")
    print("请确保服务器已启动 (运行: python app.py)")
    
    input("\n按回车键开始测试...")
    
    results = []
    
    # 测试1: 获取策略列表
    results.append(("获取策略列表", test_get_strategies()))
    
    # 测试2: 添加策略
    results.append(("添加策略", test_add_strategy()))
    
    # 测试3: 获取汇总
    results.append(("获取策略汇总", test_get_summary()))
    
    # 测试4: 生成报告
    results.append(("生成PDF报告", test_generate_report()))
    
    # 打印结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status}: {name}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！修复成功！")
    else:
        print(f"\n⚠️ 有 {total - passed} 个测试失败，请检查日志")
    
    return passed == total

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n测试被中断")
        sys.exit(1)
