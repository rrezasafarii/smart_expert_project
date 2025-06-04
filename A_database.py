from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from d_models.a_models import Base
from b_config.c_database_config import get_database_url  # 🍀 گرفتن آدرس دیتابیس
from d_models.a_models import TradingRiskSetting, Symbols, Timeframes  # 🟢 مدل‌ها

# گرفتن آدرس دیتابیس بر اساس محیط
DATABASE_URL = get_database_url()

# ساخت engine داینامیک
engine = create_engine(DATABASE_URL)

# ساخت session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_risk_settings(session):
    """
    Seed initial risk settings if the table is empty.
    """
    count = session.query(TradingRiskSetting).count()
    if count == 0:
        seed_data = [
            TradingRiskSetting(parameter_name='max_risk_percent', parameter_value='1', description='حداکثر درصد ریسک به ازای هر معامله'),
            TradingRiskSetting(parameter_name='min_lot', parameter_value='0.01', description='حداقل حجم لات مجاز'),
            TradingRiskSetting(parameter_name='max_lot', parameter_value='50', description='حداکثر حجم لات مجاز'),
            TradingRiskSetting(parameter_name='stop_loss_atr_multiplier', parameter_value='1.5', description='ضریب ATR برای تعیین فاصله حد ضرر'),
            TradingRiskSetting(parameter_name='take_profit_ratio', parameter_value='2', description='نسبت حد سود به حد ضرر (Risk/Reward)'),
        ]
        session.bulk_save_objects(seed_data)
        session.commit()
        print("✅ داده‌های اولیه تنظیمات ریسک اضافه شد.")

def seed_symbols(session):
    """
    Seed initial symbols if the table is empty.
    """
    if session.query(Symbols).count() == 0:
        symbols = [
            Symbols(symbol_name="XAUUSD", description="Gold vs US Dollar", digits=2),
            Symbols(symbol_name="USDInd", description="US Dollar Index", digits=2),
            Symbols(symbol_name="WTI", description="West Texas Intermediate Crude Oil", digits=2),
            Symbols(symbol_name="XAGUSD", description="Silver vs US Dollar", digits=3),
            Symbols(symbol_name="EURUSD", description="Euro vs US Dollar", digits=5),
            Symbols(symbol_name="US500", description="S&P 500 Index", digits=2),
        ]
        session.bulk_save_objects(symbols)
        session.commit()
        print("✅ نمادهای اولیه اضافه شدند.")

def seed_timeframes(session):
    """
    Seed initial timeframes if the table is empty.
    """
    if session.query(Timeframes).count() == 0:
        timeframes = [
            Timeframes(timeframe_name="M1", minutes=1, display_name="1 Minute"),
            Timeframes(timeframe_name="M5", minutes=5, display_name="5 Minutes"),
            Timeframes(timeframe_name="M15", minutes=15, display_name="15 Minutes"),
        ]
        session.bulk_save_objects(timeframes)
        session.commit()
        print("✅ تایم‌فریم‌های اولیه اضافه شدند.")


def init_db():
    """
    Initializes the database based on models and seeds initial data.
    """
    Base.metadata.create_all(engine)
    session = SessionLocal()
    seed_risk_settings(session)
    seed_symbols(session)       # 🟢 اضافه شده
    seed_timeframes(session)    # 🟢 اضافه شده
    session.close()
    return engine
