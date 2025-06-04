from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text, UniqueConstraint, Index,CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class AccountTypeEnum(enum.Enum):
    demo = "demo"
    real = "real"

class SignalStatusEnum(enum.Enum):
    pending = "Pending"
    executed = "Executed"
    cancelled = "Cancelled"

class PositionStatusEnum(enum.Enum):
    open = "Open"
    closed = "Closed"

class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    server = Column(String, nullable=False)
    broker = Column(String, nullable=False)
    account_type = Column(Enum(AccountTypeEnum), nullable=False)
    currency = Column(String, nullable=True)
    balance = Column(Float, default=0)
    equity = Column(Float, default=0)
    margin = Column(Float, default=0)
    leverage = Column(Integer)
    profit = Column(Float, default=0)
    free_margin = Column(Float, default=0)
    margin_level = Column(Float, nullable=True)
    investor_password = Column(String, nullable=True)
    master_password = Column(String, nullable=True)
    last_login_time = Column(DateTime, nullable=True)
    total_positions = Column(Integer, default=0)
    total_orders = Column(Integer, default=0)
    exposure = Column(Float, default=0)
    is_locked = Column(Boolean, default=False)
    last_trade_time = Column(DateTime, nullable=True)
    day_profit = Column(Float, default=0)
    week_profit = Column(Float, default=0)
    month_profit = Column(Float, default=0)
    total_profit = Column(Float, default=0)
    comment = Column(Text, nullable=True)
    platform_build = Column(Integer, nullable=True)
    trade_allowed = Column(Boolean, default=True)
    __table_args__ = (
        CheckConstraint(
            "account_type IN ('demo', 'real')",
            name="check_account_type_valid"
        ),
    )

class Symbols(Base):
    __tablename__ = 'symbols'
    id = Column(Integer, primary_key=True)
    symbol_name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    is_trading_allowed = Column(Boolean, default=True)
    digits = Column(Integer, nullable=True)
    tick_size = Column(Float, nullable=True)
    contract_size = Column(Float, nullable=True)
    margin_currency = Column(String, nullable=True)
    profit_currency = Column(String, nullable=True)
    swap_long = Column(Float, nullable=True)
    swap_short = Column(Float, nullable=True)
    lot_step = Column(Float, nullable=True)
    max_lot = Column(Float, nullable=True)
    min_lot = Column(Float, nullable=True)
    market_type = Column(String, nullable=True)

class Timeframes(Base):
    __tablename__ = 'timeframes'
    id = Column(Integer, primary_key=True)
    timeframe_name = Column(String, unique=True, nullable=False)
    minutes = Column(Integer, nullable=False)
    display_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

class Candles(Base):
    __tablename__ = 'candles'
    symbol_id = Column(Integer, ForeignKey('symbols.id'), primary_key=True)
    timeframe_id = Column(Integer, ForeignKey('timeframes.id'), primary_key=True)
    time = Column(DateTime, primary_key=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    tick_volume = Column(Integer)
    spread = Column(Integer, nullable=True)
    real_volume = Column(Integer, nullable=True)

    __table_args__ = (
        Index('ix_candles_symbol_timeframe_timestamp', 'symbol_id', 'timeframe_id', 'timestamp'),
    )

class Indicators(Base):
    __tablename__ = 'indicators'
    symbol_id = Column(Integer, ForeignKey('symbols.id'), primary_key=True)
    timeframe_id = Column(Integer, ForeignKey('timeframes.id'), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    indicator_name = Column(String, primary_key=True)
    value = Column(Float, default=0)

    __table_args__ = (
        Index('ix_indicators_symbol_timeframe_timestamp_name', 'symbol_id', 'timeframe_id', 'timestamp', 'indicator_name'),
    )

class SignalPredictions(Base):
    __tablename__ = 'signal_predictions'
    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey('symbols.id'))
    timeframe_id = Column(Integer, ForeignKey('timeframes.id'))
    timestamp = Column(DateTime, nullable=False)
    predicted_signal = Column(String, nullable=False)
    confidence = Column(Float, default=0)
    status = Column(Enum(SignalStatusEnum), default=SignalStatusEnum.pending, nullable=False)

    __table_args__ = (
        Index('ix_signal_predictions_symbol_timeframe_timestamp', 'symbol_id', 'timeframe_id', 'timestamp'),
    )

class OpenPositions(Base):
    __tablename__ = 'open_positions'
    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey('symbols.id'))
    signal_id = Column(Integer, ForeignKey('signals.id'), nullable=True)
    position_type = Column(String, nullable=False)  # BUY / SELL
    volume = Column(Float, nullable=False, default=0)
    open_price = Column(Float, nullable=False, default=0)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    open_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_price = Column(Float, nullable=True)
    close_time = Column(DateTime, nullable=True)
    profit = Column(Float, default=0)
    swap = Column(Float, nullable=False, default=0)
    status = Column(Enum(PositionStatusEnum), default=PositionStatusEnum.open, nullable=False)

    __table_args__ = (
        Index('ix_open_positions_symbol_open_time', 'symbol_id', 'open_time'),
        CheckConstraint(
            "status IN ('Open', 'Closed')",
            name="check_open_positions_status_valid"
        ),
    )

class MarketStatus(Base):
    __tablename__ = 'market_status'
    symbol_id = Column(Integer, ForeignKey('symbols.id'), primary_key=True)
    timeframe_id = Column(Integer, ForeignKey('timeframes.id'), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    trend = Column(String)
    volatility = Column(Float, default=0)
    liquidity = Column(Float, default=0)


    __table_args__ = (
        Index('ix_market_status_symbol_timeframe_timestamp', 'symbol_id', 'timeframe_id', 'timestamp'),
    )

class IndicatorWeights(Base):
    __tablename__ = 'indicator_weights'
    indicator_name = Column(String, primary_key=True)
    timeframe_id = Column(Integer, ForeignKey('timeframes.id'), primary_key=True)
    weight = Column(Float, default=1.0)

class TradingLogs(Base):
    __tablename__ = 'trading_logs'
    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey('symbols.id'))
    action_time = Column(DateTime, nullable=False)
    action = Column(String, nullable=False)  # Open/Close/Modify
    volume = Column(Float, default=0)
    price = Column(Float, default=0)
    profit = Column(Float, default=0)


    __table_args__ = (
        Index('ix_trading_logs_symbol_action_time', 'symbol_id', 'action_time'),
    )

class ModelVersions(Base):
    __tablename__ = 'model_versions'
    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    training_date = Column(DateTime, nullable=False)
    accuracy = Column(Float)
    loss = Column(Float)
    description = Column(Text)

class BacktestResults(Base):
    __tablename__ = 'backtest_results'
    id = Column(Integer, primary_key=True)
    model_version_id = Column(Integer, ForeignKey('model_versions.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    total_trades = Column(Integer)
    profit = Column(Float, default=0)
    drawdown = Column(Float, default=0)
    win_rate = Column(Float, default=0)


    __table_args__ = (
        Index('ix_backtest_results_model_version_start_date', 'model_version_id', 'start_date'),
    )

class OptimizationResults(Base):
    __tablename__ = 'optimization_results'
    id = Column(Integer, primary_key=True)
    parameter_set = Column(Text, nullable=False)
    profit = Column(Float, default=0)
    drawdown = Column(Float, default=0)
    sharpe_ratio = Column(Float, default=0)
    win_rate = Column(Float, default=0)
    test_period = Column(String)

class TradingRiskSetting(Base):
    __tablename__ = 'trading_risk_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    parameter_name = Column(String, unique=True, nullable=False)
    parameter_value = Column(String, nullable=False)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TradingRiskSetting(name={self.parameter_name}, value={self.parameter_value})>"

class Signals(Base):
    __tablename__ = 'signals'
    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey('symbols.id'))
    timeframe_id = Column(Integer, ForeignKey('timeframes.id'))
    signal_time = Column(DateTime, nullable=False)
    signal_type = Column(String, nullable=False)  # Buy / Sell
    status = Column(Enum(SignalStatusEnum), nullable=False, default=SignalStatusEnum.pending)
    entry_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    strategy_name = Column(String, nullable=True)
    execution_time = Column(DateTime, nullable=True)

    __table_args__ = (
        Index('ix_signals_symbol_timeframe_signal_time', 'symbol_id', 'timeframe_id', 'signal_time'),
        CheckConstraint(
            "status IN ('Pending', 'Executed', 'Cancelled')",
            name="check_signals_status_valid"
        ),
    )