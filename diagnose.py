# -*- coding: utf-8 -*-
"""
诊断脚本 - 找出卡顿的真正原因
"""
import sys
import time
import traceback

# 添加项目路径
sys.path.insert(0, '.')

def test_strategy_manager():
    """测试策略管理器"""
    print("\n=== 测试策略管理器 ===")
    try:
        from modules.strategy_manager import StrategyManager
        
        manager = StrategyManager()
        
        # 测试获取策略列表
        print("1. 测试获取策略列表...")
        start = time.time()
        conn = manager._StrategyManager__get_db_conn() if hasattr(manager, '_StrategyManager__get_db_conn') else None
        if conn:
            conn.close()
        
        import sqlite3
        db_path = manager.db_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM strategies')
        count = cursor.fetchone()[0]
        print(f"   策略数量: {count}")
        conn.close()
        
        # 测试获取汇总数据
        print("2. 测试获取汇总数据...")
        start = time.time()
        data = manager.get_summary_data()
        elapsed = time.time() - start
        print(f"   耗时: {elapsed:.2f}秒")
        print(f"   策略数: {len(data.get('strategies', []))}")
        
        return True
    except Exception as e:
        print(f"   错误: {e}")
        traceback.print_exc()
        return False

def test_basis_chart():
    """测试基差图表生成"""
    print("\n=== 测试基差图表生成 ===")
    try:
        from modules.basis_chart_generator import BasisChartGenerator
        import sqlite3
        import os
        
        generator = BasisChartGenerator()
        
        # 获取第一个策略
        db_path = generator.db_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM strategies LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            print("   没有策略，跳过测试")
            return True
        
        columns = ['id', 'strategy_code', 'strategy_name', 'strategy_type', 'business_type',
                   'futures_contract', 'futures_contract2', 'spot_variety', 'forward_variety',
                   'futures_direction', 'spot_direction', 'plan_quantity', 'apply_org',
                   'apply_person', 'apply_date', 'valid_until', 'current_basis', 'sort_order']
        strategy = dict(zip(columns, row))
        
        print(f"   测试策略: {strategy['strategy_code']}")
        
        # 测试获取基差数据
        print("   测试获取基差数据...")
        start = time.time()
        basis_data = generator._get_basis_data(strategy)
        elapsed = time.time() - start
        print(f"   耗时: {elapsed:.2f}秒")
        if basis_data:
            print(f"   数据点数: {len(basis_data)}")
        else:
            print("   无数据")
        
        # 测试生成图表
        print("   测试生成图表...")
        import tempfile
        output_path = os.path.join(tempfile.gettempdir(), f"test_chart_{int(time.time())}.png")
        start = time.time()
        result = generator.generate_basis_chart(strategy, output_path)
        elapsed = time.time() - start
        print(f"   耗时: {elapsed:.2f}秒")
        print(f"   结果: {'成功' if result else '失败'}")
        
        # 清理
        if os.path.exists(output_path):
            os.remove(output_path)
        
        return True
    except Exception as e:
        print(f"   错误: {e}")
        traceback.print_exc()
        return False

def test_data_files():
    """测试数据文件"""
    print("\n=== 测试数据文件 ===")
    try:
        import sqlite3
        import os
        
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'strategy.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT file_type, file_name, file_path FROM data_files ORDER BY upload_date DESC")
        files = cursor.fetchall()
        conn.close()
        
        print(f"   已上传文件数: {len(files)}")
        
        for file_type, file_name, file_path in files:
            exists = os.path.exists(file_path)
            size = os.path.getsize(file_path) if exists else 0
            print(f"   - {file_type}: {file_name} ({'存在' if exists else '不存在'}, {size/1024:.1f}KB)")
        
        return True
    except Exception as e:
        print(f"   错误: {e}")
        return False

def test_report_generation():
    """测试报告生成"""
    print("\n=== 测试报告生成流程 ===")
    try:
        from modules.strategy_manager import StrategyManager
        from modules.basis_chart_generator import BasisChartGenerator
        import sqlite3
        import os
        import tempfile
        
        manager = StrategyManager()
        chart_gen = BasisChartGenerator()
        
        # 获取所有策略
        db_path = manager.db_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM strategies')
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        
        strategies = [dict(zip(columns, row)) for row in rows]
        print(f"   策略总数: {len(strategies)}")
        
        if not strategies:
            print("   没有策略，跳过测试")
            return True
        
        # 只测试前3个策略
        test_strategies = strategies[:3]
        print(f"   测试策略数: {len(test_strategies)}")
        
        # 测试获取复盘数据
        print("   测试获取复盘数据...")
        start = time.time()
        all_weekly_data = manager.get_all_strategies_weekly_data(test_strategies)
        elapsed = time.time() - start
        print(f"   耗时: {elapsed:.2f}秒")
        
        # 测试生成图表
        print("   测试生成图表...")
        chart_images = {}
        for strategy in test_strategies:
            strategy_id = strategy['id']
            output_path = os.path.join(tempfile.gettempdir(), f"test_chart_{strategy_id}_{int(time.time())}.png")
            
            start = time.time()
            result = chart_gen.generate_basis_chart(strategy, output_path)
            elapsed = time.time() - start
            
            print(f"     {strategy['strategy_code']}: {'成功' if result else '失败'}, 耗时{elapsed:.2f}秒")
            
            if result:
                chart_images[strategy_id] = output_path
            
            # 清理
            if os.path.exists(output_path):
                os.remove(output_path)
        
        return True
    except Exception as e:
        print(f"   错误: {e}")
        traceback.print_exc()
        return False

def check_infinite_loop():
    """检查可能的死循环"""
    print("\n=== 检查循环问题 ===")
    
    # 检查strategy_manager.py中的循环
    print("1. 检查代码中的循环...")
    
    with open('modules/strategy_manager.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有明显的循环问题
    if 'while True' in content:
        print("   警告: 发现 while True 循环")
    else:
        print("   未发现 while True 循环")
    
    # 检查递归调用
    if content.count('def get_summary_data') > 1:
        print("   警告: get_summary_data 定义了多次")
    else:
        print("   函数定义正常")
    
    return True

def main():
    print("=" * 60)
    print("期现交易策略汇报软件 - 诊断工具")
    print("=" * 60)
    
    results = []
    
    # 运行各项测试
    results.append(("数据文件检查", test_data_files()))
    results.append(("策略管理器", test_strategy_manager()))
    results.append(("基差图表生成", test_basis_chart()))
    results.append(("报告生成流程", test_report_generation()))
    results.append(("循环问题检查", check_infinite_loop()))
    
    # 汇总
    print("\n" + "=" * 60)
    print("诊断结果")
    print("=" * 60)
    
    for name, result in results:
        status = "通过" if result else "失败"
        print(f"  [{status}] {name}")
    
    print("\n请根据以上结果判断问题所在。")

if __name__ == '__main__':
    main()
