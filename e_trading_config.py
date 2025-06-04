
import sqlite3
from decimal import Decimal
from b_config.f_logger_config import get_logger
from pathlib import Path

class TradingRiskConfig:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = get_logger('risk_manager', level='DEBUG')
        self.settings = self.load_risk_settings()

    def load_risk_settings(self):
        """Load risk parameters from database into a dictionary."""
        settings = {}
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT parameter_name, parameter_value FROM trading_risk_settings")
        for name, value in cursor.fetchall():
            settings[name] = value
        conn.close()
        self.logger.info(f"تنظیمات ریسک بارگذاری شد: {settings}")
        return settings

    def calculate_position_size(self, balance: float, entry_price: float, stop_loss_price: float):
        """Calculate the optimal position size based on risk settings."""
        risk_percent = float(self.settings.get('max_risk_percent', 1)) / 100
        risk_amount = balance * risk_percent
        risk_per_unit = abs(entry_price - stop_loss_price)
        if risk_per_unit == 0:
            self.logger.error("اختلاف قیمت ورود و حد ضرر صفر است، محاسبه حجم غیرممکن.")
            return 0
        volume = risk_amount / risk_per_unit
        min_lot = float(self.settings.get('min_lot', 0.01))
        max_lot = float(self.settings.get('max_lot', 50))
        volume = max(min(volume, max_lot), min_lot)
        self.logger.info(f"حجم محاسبه شده: {volume} لات برای ریسک مجاز: {risk_percent*100}%")
        return round(volume, 2)

    def calculate_sl_tp(self, entry_price: float):
        """Calculate Stop Loss and Take Profit based on dynamic strategy."""
        atr_multiplier = float(self.settings.get('stop_loss_atr_multiplier', 1.5))
        atr_value = 20  # فرضی — در پروژه واقعی این مقدار از اندیکاتور گرفته می‌شود
        sl_distance = atr_multiplier * atr_value
        tp_distance = sl_distance * float(self.settings.get('take_profit_ratio', 2))

        stop_loss = entry_price - sl_distance
        take_profit = entry_price + tp_distance
        self.logger.info(f"SL: {stop_loss}, TP: {take_profit} برای قیمت ورود: {entry_price}")
        return stop_loss, take_profit

    def is_position_allowed(self, open_positions: int):
        """Check if a new position is allowed."""
        if open_positions >= 1:
            self.logger.warning("مجاز به باز کردن پوزیشن جدید نیستید. فقط یک پوزیشن همزمان مجاز است.")
            return False
        self.logger.info("باز کردن پوزیشن جدید مجاز است.")
        return True
