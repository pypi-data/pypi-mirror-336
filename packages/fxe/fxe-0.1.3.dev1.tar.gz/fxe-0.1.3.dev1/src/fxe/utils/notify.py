import os

import pandas as pd
import requests
from finlab.core.report import Report as ReportPyx


def tg_notify(
    self: ReportPyx,
    telegram_token: str = "",
    chat_id: str = "",
    parse_mode: str = "Markdown",
    name: str = "",
):
    """
    Send a notification message to Telegram with position and strategy information.

        This function formats and sends a message to a Telegram chat containing:
        1. Current strategy list with entry dates and prices
        2. Recent operations including new entries and exits

            self (ReportPyx): The backtest report instance containing trade information
            telegram_token (str, optional): Telegram bot API token. Defaults to "".
            chat_id (str, optional): Target Telegram chat ID. Defaults to "".
            parse_mode (str, optional): Telegram message parse mode. Defaults to "Markdown".
            name (str, optional): Strategy name or identifier to be included in the message. Defaults to "".

            Exception: If the provided self parameter is not a valid ReportPyx instance.

        Returns:
            None: The function prints the Telegram API response but doesn't return any value.

        Example:
            >>> report.tg_notify(
            ...     telegram_token="your_token",
            ...     chat_id="your_chat_id",
            ...     name="Strategy A"
            ...
    """

    # Check if chat_id and telegram_token are provided or available in environment variables

    if not telegram_token:
        telegram_token = os.environ.get("TELEGRAM_TOKEN")
        if not telegram_token:
            raise ValueError(
                "Telegram token must be provided either as an argument or in TELEGRAM_TOKEN environment variable"
            )

    if not chat_id:
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not chat_id:
            raise ValueError(
                "Chat ID must be provided either as an argument or in TELEGRAM_CHAT_ID environment variable"
            )

    if not isinstance(self, ReportPyx):
        raise Exception("Please provide a valid backtest report.")
    hold = []
    enter = []
    exit = []
    for i, p in self.position_info().items():
        if isinstance(p, dict):
            if i[:4].isdigit():
                if "*" in i:
                    i = i.replace("*", r"\*")
                if p["status"] in ["exit"] and pd.isnull(self.current_trades.loc[i].exit_date):
                    hold.append(f"{i}: {p['entry_date'][:10]}, {str(p['entry_price'])}")
                if p["status"] in ["hold", "sl", "tp"]:
                    hold.append(f"{i}: {p['entry_date'][:10]}, {str(p['entry_price'])}")
                if p["status"] in ["enter"]:
                    enter.append(f"{i}: {p['entry_date'][:10]}的下個交易日進場")
                if p["status"] in ["exit", "sl", "tp"]:
                    exit.append(f"{i}: {p['exit_date'][:10]}的下個交易日出場")
    message_lines = [f"{name}: 目前策略清單 進場日及進場價格："]
    message_lines.extend(hold)
    message_lines.append("------------------------------")
    message_lines.append("近期操作：")
    message_lines.append("-策略新增")
    if len(enter) > 0:
        message_lines.extend(enter)
    else:
        message_lines.append("尚無")
    message_lines.append("-策略移除")
    if len(exit) > 0:
        message_lines.extend(exit)
    else:
        message_lines.append("尚無")
    message = "\n".join(message_lines)

    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}
    response = requests.post(url, json=payload)
    print(response.json())


def extend_finlab() -> None:
    ReportPyx.tg_notify = tg_notify
