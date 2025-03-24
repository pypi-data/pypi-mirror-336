from typing import Any, dict, list, tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def calculate_returns(
    prices: pd.Series,
    method: str = "simple"
) -> pd.Series:
    """計算報酬率序列。

    提供簡單報酬率和對數報酬率兩種計算方式。

    Args:
        prices: 價格序列。
        method: 計算方法，可選 "simple" 或 "log"。

    Returns:
        報酬率序列。

    Raises:
        ValueError: 當 method 不是 "simple" 或 "log" 時。

    Examples:
        >>> prices = pd.Series([100, 110, 105])
        >>> returns = calculate_returns(prices, "simple")
        >>> returns.round(3)
        0     NaN
        1    0.100
        2   -0.045
        dtype: float64

        >>> returns = calculate_returns(prices, "log")
        >>> returns.round(3)
        0     NaN
        1    0.095
        2   -0.047
        dtype: float64
    """
    if method not in ["simple", "log"]:
        raise ValueError("method must be 'simple' or 'log'")

    if method == "simple":
        return prices.pct_change()
    else:
        return np.log(prices / prices.shift(1))


class PortfolioAnalyzer:
    """投資組合分析工具。

    用於計算各種投資組合績效指標。

    Attributes:
        returns: 投資組合報酬率序列。
        benchmark_returns: 大盤指數報酬率序列。
        risk_free_rate: 年化無風險利率。

    Examples:
        >>> returns = pd.Series([0.01, -0.02, 0.03])
        >>> benchmark = pd.Series([0.005, -0.01, 0.02])
        >>> analyzer = PortfolioAnalyzer(returns, benchmark, 0.02)
        >>> analyzer.sharpe_ratio > 0
        True
    """

    def __init__(
        self,
        returns: pd.Series,
        benchmark_returns: pd.Series,
        risk_free_rate: float = 0.02
    ) -> None:
        """初始化投資組合分析器。

        Args:
            returns: 投資組合報酬率序列。
            benchmark_returns: 大盤指數報酬率序列。
            risk_free_rate: 年化無風險利率，預設為 2%。
        """
        self.returns = returns
        self.benchmark_returns = benchmark_returns
        self.risk_free_rate = risk_free_rate

    def calculate_metrics(self) -> dict[str, float]:
        """計算績效指標。

        Returns:
            包含以下鍵值的字典：
                - sharpe_ratio: 夏普比率
                - sortino_ratio: 索提諾比率
                - max_drawdown: 最大回撤
                - alpha: Jensen's Alpha
                - beta: 貝塔係數
                - information_ratio: 資訊比率

        Examples:
            >>> returns = pd.Series([0.01, -0.02, 0.03])
            >>> benchmark = pd.Series([0.005, -0.01, 0.02])
            >>> analyzer = PortfolioAnalyzer(returns, benchmark)
            >>> metrics = analyzer.calculate_metrics()
            >>> all(isinstance(v, float) for v in metrics.values())
            True
        """
        return {
            "sharpe_ratio": self._calculate_sharpe_ratio(),
            "max_drawdown": self._calculate_max_drawdown()
        }


def validate_stock_data(
    data: pd.DataFrame,
    required_columns: list[str] | None = None
) -> tuple[bool, str]:
    """驗證股票資料的完整性。

    Args:
        data: 股票資料框。
        required_columns: 必要欄位列表，如果為 None，
            則使用預設值 ["open", "high", "low", "close", "volume"]。

    Returns:
        (bool, str) tuple:
            - bool: 驗證是否通過
            - str: 錯誤訊息，如果驗證通過則為空字串

    Examples:
        基本使用:
        >>> df = pd.DataFrame({
        ...     "close": [100, 101],
        ...     "volume": [1000, 1100]
        ... })
        >>> is_valid, msg = validate_stock_data(df, ["close", "volume"])
        >>> is_valid
        True

        缺少必要欄位:
        >>> df = pd.DataFrame({"close": [100, 101]})
        >>> is_valid, msg = validate_stock_data(df, ["close", "volume"])
        >>> is_valid
        False
        >>> "volume" in msg.lower()
        True
    """
    if required_columns is None:
        required_columns = ["open", "high", "low", "close", "volume"]

    missing_columns = [col for col in required_columns if col not in data.columns]

    if missing_columns:
        return False, f"缺少必要欄位: {', '.join(missing_columns)}"

    return True, ""


def plot_technical_chart(
    df: pd.DataFrame,
    indicators: dict[str, pd.Series] | None = None
) -> go.Figure:
    """繪製技術分析圖表。

    Args:
        df: 包含 OHLCV 資料的 DataFrame。
        indicators: 技術指標字典，鍵為指標名稱，值為指標數據。

    Returns:
        plotly 圖表物件。

    Examples:
        >>> df = pd.DataFrame({
        ...     'open': [100, 101], 'high': [102, 103],
        ...     'low': [99, 100], 'close': [101, 102],
        ...     'volume': [1000, 1100]
        ... })
        >>> fig = plot_technical_chart(df)
        >>> isinstance(fig, go.Figure)
        True

        添加技術指標：
        >>> sma = pd.Series([100.5, 101.5])
        >>> fig = plot_technical_chart(df, {'SMA': sma})
        >>> isinstance(fig, go.Figure)
        True
    """
    return go.Figure()  # 實際實作省略


async def fetch_market_data(
    symbols: list[str],
    start_date: str,
    end_date: str,
    api_key: str | None = None
) -> dict[str, pd.DataFrame]:
    """從外部 API 獲取市場資料。

    非同步獲取多個商品的歷史價格資料。

    Args:
        symbols: 商品代碼列表。
        start_date: 起始日期，格式 'YYYY-MM-DD'。
        end_date: 結束日期，格式 'YYYY-MM-DD'。
        api_key: API 金鑰，預設為 None，將使用環境變數。

    Returns:
        字典，鍵為商品代碼，值為對應的價格資料框。

    Raises:
        APIError: 當 API 請求失敗時。
        ValueError: 當日期格式不正確時。

    Examples:
        基本使用：
        >>> symbols = ['2330', '2317']
        >>> async with aiohttp.ClientSession() as session:
        ...     data = await fetch_market_data(
        ...         symbols,
        ...         '2023-01-01',
        ...         '2023-12-31'
        ...     )
        >>> print(f"獲取到 {len(data)} 檔股票的資料")

        使用自訂 API 金鑰：
        >>> data = await fetch_market_data(
        ...     symbols,
        ...     '2023-01-01',
        ...     '2023-12-31',
        ...     api_key='your-api-key'
        ... )
    """


def calculate_metrics(
    returns: pd.Series,
    benchmark: pd.Series,
    risk_free: float = 0.03
) -> dict[str, float]:
    """計算投資組合績效指標。

    計算包括夏普比率、最大回撤等關鍵績效指標。

    Args:
        returns: 投資組合日報酬率序列。
        benchmark: 大盤指數日報酬率序列。
        risk_free: 無風險利率，年化，預設為 3%。

    Returns:
        包含以下鍵值的字典：
            - sharpe_ratio: 夏普比率
            - max_drawdown: 最大回撤
            - alpha: Jensen's Alpha
            - beta: 系統性風險
            - information_ratio: 資訊比率

    Examples:
        基本使用：
        >>> returns = pd.Series([0.01, -0.02, 0.03])
        >>> benchmark = pd.Series([0.005, -0.01, 0.02])
        >>> metrics = calculate_metrics(returns, benchmark)
        >>> print(f"夏普比率: {metrics['sharpe_ratio']:.2f}")
        夏普比率: 1.25

        使用自訂無風險利率：
        >>> metrics = calculate_metrics(returns, benchmark, risk_free=0.02)
    """


class Strategy:
    """交易策略基礎類別。

    此類別提供建立交易策略的基本框架，包含信號生成和部位管理。

    Attributes:
        name: 策略名稱。
        parameters: 策略參數字典。
        position: 目前持倉部位。

    Note:
        繼承此類別時需實作 generate_signals 方法。

    Examples:
        >>> class MyStrategy(Strategy):
        ...     def generate_signals(self, data):
        ...         # 實作信號生成邏輯
        ...         return signals
        ...
        >>> strategy = MyStrategy("均線交叉", {"fast": 5, "slow": 20})
        >>> strategy.run(data)
    """

    def __init__(self, name: str, parameters: dict[str, Any]) -> None:
        """初始化策略。

        Args:
            name: 策略名稱。
            parameters: 策略參數字典。
        """


class StrategyV2:
    """量化交易策略基礎類別。

    此類別提供建立交易策略的基本框架。

    Attributes:
        name: 策略名稱
        description: 策略描述
        parameters: 策略參數

    Examples:
        >>> strategy = Strategy("均線交叉", "使用 20/60 均線交叉產生交易訊號")
        >>> strategy.set_parameters({"short": 20, "long": 60})
    """

    def __init__(self, name: str, description: str | None = None) -> None:
        self.name = name
        self.description = description
        self.parameters = {}

    def set_parameters(self, params: dict) -> None:
        """設定策略參數。

        Args:
            params: 參數字典，包含策略所需的所有參數

        Raises:
            ValueError: 如果參數格式不正確
        """
        self.parameters.update(params)


def process_stock_data(
    df: pd.DataFrame,
    window: int = 20,
    method: str = "sma"
) -> pd.DataFrame:
    """計算技術指標。

    針對股價資料計算技術指標，支援多種計算方法。

    Args:
        df: 股價資料框，需包含 'close' 欄位。
        window: 計算窗口大小，預設為 20。
        method: 計算方法，可選 "sma"（簡單移動平均）或 "ema"（指數移動平均）。

    Returns:
        DataFrame 包含原始資料和計算後的技術指標。

    Raises:
        ValueError: 當 method 不是支援的計算方法時。
        KeyError: 當輸入資料框缺少必要欄位時。

    Examples:
        >>> prices = pd.DataFrame({'close': [100, 101, 102, 103, 104]})
        >>> process_stock_data(prices, window=3, method="sma")
           close    sma
        0    100    NaN
        1    101    NaN
        2    102  101.0
        3    103  102.0
        4    104  103.0
    """
