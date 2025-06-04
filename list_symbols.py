import MetaTrader5 as mt5

mt5.initialize()

symbol = "XAUUSD"  # یا XAUUSD
timeframe = mt5.TIMEFRAME_M15

rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)

if rates is None:
    print("⛔ دیتایی وجود نداره.")
else:
    print(rates)

mt5.shutdown()
