# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from modules.strategy_manager import StrategyManager

strategy = {
    'strategy_type': '套期保值',
    'business_type': '期货-现货',
    'futures_contract': 'RB2605',
    'spot_variety': '马钢螺纹',
    'futures_direction': '空'
}

sm = StrategyManager()
result = sm.calculate_strategy_summary(strategy)

print("=== 策略汇总计算结果 ===")
print(f"持仓数量: {result['position_quantity']} 吨")
print(f"持仓盈亏: {result['position_profit']:,.2f} 元")
print(f"平仓数量: {result['close_quantity']} 吨")
print(f"平仓盈亏: {result['close_profit']:,.2f} 元")
print()
print("说明：")
print("- 平仓盈亏 = (开仓价 - 平仓价) × 平仓手数 × 10吨 [卖出套保]")
print("- 持仓盈亏 = 持仓手数 × 10吨 × (当前基差 - 建仓基差) [卖出套保]")
