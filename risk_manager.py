# risk_manager.py
"""
(核心组件 - 风控)
职责：独立封装风控逻辑，确保单一职责原则。


来源参考： (RiskManager 类)
"""

from loguru import logger

class RiskManager:
    def __init__(self, initial_cash):
        self.max_drawdown = 0.10
        self.max_per_asset = 0.35
        self.daily_loss_limit = 0.04
        self.peak = float(initial_cash or 0)
        self.initial_cash = float(initial_cash or 0)
        self.today_pnl = 0.0

    def check(self, total_value: float, positions: dict) -> bool:
        # 更新峰值
        self.peak = max(self.peak, total_value)
        
        # 1. 最大回撤检查
        drawdown = (self.peak - total_value) / self.peak
        if drawdown > self.max_drawdown:
            logger.warning(f"风控触发：最大回撤 {drawdown:.2%} 超限")
            return False

        # 2. 单资产暴露检查
        for sym, value in positions.items():
            if value / total_value > self.max_per_asset:
                logger.warning(f"风控触发：{sym} 单币暴露超 35%")
                return False

        # 3. 每日亏损熔断 (简化逻辑，实际可能需要重置逻辑)
        current_pnl = total_value - self.initial_cash
        if current_pnl < -self.daily_loss_limit * self.initial_cash:
            logger.warning("风控触发：当日亏损超 4%")
            return False

        return True