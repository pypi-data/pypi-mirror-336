import logging

import numpy as np  # noqa: F401
import pandas as pd
from finlab import data
from finlab.core.report import Report as ReportPyx

logger = logging.getLogger(__name__)


def omega_ratio(self: ReportPyx, benchmark_ret: pd.Series = None) -> float:
    """
    Calculate the Omega ratio of the strategy returns against a benchmark.

    The Omega ratio measures the probability-weighted ratio of gains versus
    losses for a given threshold (in this case, benchmark returns).

    Args:
        self: The ReportPyx instance containing strategy returns.
        benchmark_ret: Optional benchmark returns series. If None, uses Taiwan weighted index.

    Returns:
        float: The calculated Omega ratio. Returns infinity if there are no losses.

    Examples:
        >>> report = sim(...)  # strategy report
        >>> ratio = report.omega_ratio()
        >>> print(f"Omega Ratio: {ratio:.2f}")
        >>> strategy_reports = { "strategy": r1, }
        >>> omega_scores = { name: omega_ratio(rpt, benchmark_returns) for name, rpt in strategy_reports.items() }
        >>> omega_df = pd.Series(omega_scores).sort_values(ascending=False)
        >>> print("📊 各策略對大盤的 Omega Ratio 排行榜：\n")
        >>> print(omega_df)

    Raises:
        ValueError: If benchmark data cannot be retrieved or calculations fail.
    """
    try:
        # Get benchmark returns if not provided
        if benchmark_ret is None:
            try:
                benchmark = data.get("benchmark_return:發行量加權股價報酬指數").squeeze()
                benchmark_ret = benchmark.pct_change()
            except Exception as e:
                logger.error(f"Failed to get benchmark returns: {str(e)}")
                raise ValueError("Could not retrieve benchmark data") from e

        # Calculate strategy returns and align with benchmark
        strategy_returns = self.creturn.pct_change()
        aligned_returns = pd.concat([strategy_returns, benchmark_ret], axis=1).dropna()

        # Calculate excess returns
        excess_returns = aligned_returns.iloc[:, 0] - aligned_returns.iloc[:, 1]

        # Calculate positive and negative sums
        positive_sum = excess_returns[excess_returns > 0].sum()
        negative_sum = -excess_returns[excess_returns < 0].sum()

        # Return ratio or infinity
        return float("inf") if negative_sum == 0 else positive_sum / negative_sum

    except Exception as e:
        logger.error(f"Error calculating Omega ratio: {str(e)}")
        raise


def extend_finlab() -> None:
    ReportPyx.omega_ratio = omega_ratio
