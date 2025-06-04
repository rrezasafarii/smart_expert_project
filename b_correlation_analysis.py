import sqlite3
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def load_close_prices(conn, timeframe_id):
    """بارگذاری قیمت بسته شدن برای همه نمادها در تایم‌فریم مشخص"""
    query = """
        SELECT s.symbol_name, c.time, c.close
        FROM candles c
        JOIN symbols s ON c.symbol_id = s.id
        WHERE c.timeframe_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(timeframe_id,))
    return df

def pivot_close_prices(df):
    """Pivot دیتا به فرمت wide: timestamps به عنوان اندیس و نمادها به عنوان ستون‌ها"""
    df_pivot = df.pivot(index='time', columns='symbol_name', values='close')
    df_pivot = df_pivot.dropna()  # حذف ردیف‌هایی که دیتای کامل ندارن
    return df_pivot

def calculate_returns(df_pivot):
    """محاسبه returns برای هر نماد"""
    returns = df_pivot.pct_change().dropna()  # درصد تغییرات بین کندل‌ها
    return returns

def calculate_correlation(df_returns):
    """محاسبه ماتریس همبستگی روی returns"""
    correlation_matrix = df_returns.corr()
    return correlation_matrix

def plot_correlation_heatmap(correlation_matrix, title):
    """رسم Heatmap همبستگی"""
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title(title)
    plt.show()

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, "..", "c_database", "smart_expert.db")

    conn = connect_db(db_path)

    timeframe_id = 3  # M15 تایم‌فریم

    # بارگذاری دیتا
    df = load_close_prices(conn, timeframe_id)
    print(f"✅ {len(df)} ردیف دیتا بارگذاری شد.")

    # Pivot دیتا
    df_pivot = pivot_close_prices(df)
    print(f"✅ دیتا Pivot شد با شکل {df_pivot.shape}.")

    # محاسبه returns
    df_returns = calculate_returns(df_pivot)
    print(f"✅ Returns محاسبه شد با شکل {df_returns.shape}.")

    # محاسبه همبستگی returns
    correlation_matrix = calculate_correlation(df_returns)
    print("✅ ماتریس همبستگی روی Returns محاسبه شد.")

    # رسم Heatmap
    plot_correlation_heatmap(correlation_matrix, "Correlation Matrix of Returns")

    conn.close()
    print("✅ اتصال به دیتابیس بسته شد.")

if __name__ == "__main__":
    main()
