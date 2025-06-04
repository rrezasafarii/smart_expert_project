import sys
import os
import subprocess
import logging
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# پکیج‌های لازم
required_packages = [
    "sqlalchemy", "pandas", "numpy", "scikit-learn", "xgboost", "lightgbm", "matplotlib",
    "seaborn", "plotly", "optuna", "catboost", "fastapi", "uvicorn", "pydantic", "mlflow",
    "joblib", "tqdm", "gym", "transformers", "scipy", "pycaret", "statsmodels", "MetaTrader5"
]

def install_packages(packages):
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} already installed.")
        except ImportError:
            print(f"📦 Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError:
                print(f"⚠️  Regular install failed for {package}, trying with --user...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])

def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def load_close_prices(conn, timeframe_id):
    query = """
        SELECT s.symbol_name, c.time, c.close
        FROM candles c
        JOIN symbols s ON c.symbol_id = s.id
        WHERE c.timeframe_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(timeframe_id,))
    return df

def pivot_close_prices(df):
    df_pivot = df.pivot(index='time', columns='symbol_name', values='close')
    df_pivot = df_pivot.dropna()
    return df_pivot

def calculate_returns(df_pivot):
    returns = df_pivot.pct_change().dropna()
    return returns

def calculate_correlation(df_returns):
    correlation_matrix = df_returns.corr()
    return correlation_matrix

def plot_correlation_heatmap(correlation_matrix, title):
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title(title)
    plt.show()

def calculate_rolling_correlation(df_returns, symbol1, symbol2, window=100):
    rolling_corr = df_returns[symbol1].rolling(window).corr(df_returns[symbol2])
    return rolling_corr

def plot_rolling_correlation(rolling_corr, symbol1, symbol2):
    plt.figure(figsize=(12, 6))
    rolling_corr.plot()
    plt.title(f'Rolling Correlation ({symbol1} vs {symbol2})')
    plt.xlabel('Time')
    plt.ylabel('Correlation')
    plt.grid(True)
    plt.show()

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    install_packages(required_packages)

    from b_config.f_logger_config import get_logger
    logger = get_logger('main', level=logging.DEBUG)
    logger.info("شروع اجرای پروژه Smart Expert")

    from c_database.a_database import init_db
    try:
        engine = init_db()
        logger.info("✅ دیتابیس ساخته شد و داده‌های اولیه اضافه شدند.")
    except Exception as e:
        logger.error(f"❌ خطا در ساخت دیتابیس: {e}")
        sys.exit(1)

    try:
        from e_data_ingestion.a_fetch_candles import main_fetch
        main_fetch()  # کشیدن کندل‌ها
        logger.info("✅ کشیدن کندل‌ها با موفقیت انجام شد.")
    except Exception as e:
        logger.error(f"❌ خطا در کشیدن کندل‌ها: {e}")
        sys.exit(1)

    # 🟢 تحلیل Correlation بعد از کشیدن کندل‌ها
    try:
        logger.info("🚀 شروع تحلیل Correlation و Rolling Correlation...")

        db_path = os.path.join(base_path, "c_database", "smart_expert.db")
        conn = connect_db(db_path)

        timeframe_id = 3  # M15

        df = load_close_prices(conn, timeframe_id)
        df_pivot = pivot_close_prices(df)
        df_returns = calculate_returns(df_pivot)
        correlation_matrix = calculate_correlation(df_returns)

        plot_correlation_heatmap(correlation_matrix, "Correlation Matrix of Returns")

        symbol1 = "XAUUSD"
        symbol2 = "USDInd"
        rolling_corr = calculate_rolling_correlation(df_returns, symbol1, symbol2, window=100)
        plot_rolling_correlation(rolling_corr, symbol1, symbol2)

        conn.close()
        logger.info("✅ تحلیل Correlation انجام شد.")
    except Exception as e:
        logger.error(f"❌ خطا در تحلیل Correlation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
