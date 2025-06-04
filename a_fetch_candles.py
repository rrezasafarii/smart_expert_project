import MetaTrader5 as mt5
import sqlite3
import pandas as pd
from datetime import datetime
import os

def connect_mt5():
    """اتصال به متاتریدر 5"""
    if not mt5.initialize():
        raise Exception(f"❌ اتصال به متاتریدر 5 برقرار نشد: {mt5.last_error()}")
    print("✅ اتصال موفق به متاتریدر 5")

def connect_db(db_path):
    """اتصال به دیتابیس SQLite"""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"❌ فایل دیتابیس پیدا نشد: {db_path}")
    conn = sqlite3.connect(db_path)
    print("✅ اتصال موفق به دیتابیس")
    return conn

def fetch_candles(symbol, timeframe, num_candles):
    """دریافت کندل‌ها از MT5 بدون تکراری"""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if rates is None or len(rates) == 0:
        raise Exception(f"❌ هیچ دیتایی برنگشت برای {symbol} در تایم‌فریم {timeframe}")
    df = pd.DataFrame(rates)
    df['timestamp'] = pd.to_datetime(df['time'], unit='s')
    df = df.drop_duplicates(subset=['timestamp'])  # حذف دابل
    return df

def save_candles_to_db(candles_df, symbol_id, timeframe_id, conn):
    """ذخیره کندل‌ها در دیتابیس"""
    cursor = conn.cursor()
    for index, row in candles_df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO candles (symbol_id, timeframe_id, time, open, high, low, close, tick_volume, spread, real_volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            symbol_id,
            timeframe_id,
            row['timestamp'].to_pydatetime(),
            row['open'],
            row['high'],
            row['low'],
            row['close'],
            row['tick_volume'],
            row['spread'],
            row['real_volume']
        ))
    conn.commit()
    print(f"✅ {len(candles_df)} کندل جدید برای نماد {symbol_id} ذخیره شد.")

# تعریف تایم‌فریم‌های استاندارد MT5
TIMEFRAMES = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15
}

# تعداد کندل‌هایی که میخوایم بکشیم برای هر تایم‌فریم
CANDLE_COUNTS = {
    "M1": 14400,  # 10 روز کاری برای M1
    "M5": 2880,   # 10 روز کاری برای M5
    "M15": 960    # 10 روز کاری برای M15
}

def tf_name_to_id(tf_name):
    """تبدیل اسم تایم‌فریم به ID جدول Timeframes"""
    mapping = {"M1": 1, "M5": 2, "M15": 3}
    return mapping[tf_name]

def run_fetch_for_symbol(symbol, symbol_id, db_path):
    """کشیدن دیتا برای هر نماد و هر تایم‌فریم"""
    conn = connect_db(db_path)
    try:
        for tf_name, tf_code in TIMEFRAMES.items():
            print(f"🚀 در حال کشیدن {CANDLE_COUNTS[tf_name]} کندل برای {symbol} در {tf_name}")
            candles_df = fetch_candles(symbol, tf_code, CANDLE_COUNTS[tf_name])
            save_candles_to_db(candles_df, symbol_id, tf_name_to_id(tf_name), conn)
    finally:
        conn.close()
        print(f"✅ اتصال به دیتابیس بسته شد برای نماد {symbol}")

def main_fetch():
    """اجرای کامل برای همه نمادهای همبستگی"""
    connect_mt5()

    # آدرس فایل دیتابیس
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "c_database", "smart_expert.db")

    # لیست نمادها و ID ها
    symbols_to_fetch = {
        "XAUUSD": 1,
        "USDInd": 2,
        "WTI": 3,
        "XAGUSD": 4,
        "EURUSD": 5,
        "US500": 6
    }

    for symbol, symbol_id in symbols_to_fetch.items():
        run_fetch_for_symbol(symbol, symbol_id, db_path)

    mt5.shutdown()
    print("🔕 اتصال به متاتریدر 5 بسته شد.")
