# FXE (Finlab Extension Tool)

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## 專案簡介

FXE 是一個擴展 Finlab 功能的工具集，提供更多進階的量化交易功能。

## 主要功能

* 策略開發輔助工具
* 資料分析增強功能
* 回測結果視覺化
* 客製化技術指標

## 快速開始

### 安裝

```bash
pip install fxe
```

### 基本使用

```python
from fxe import strategy

# 建立策略
strategy = strategy.create(
    entry="close > sma(close, 20)",
    exit="close < sma(close, 60)"
)

# 執行回測
result = strategy.backtest()
```

## 文件導覽

* [安裝指南](installation.md) - 詳細的安裝說明
* [使用教學](tutorials/index.md) - 從基礎開始的教學
* [進階指南](guide/index.md) - 進階功能說明

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

```bash
src
└── fxe
    ├── __init__.py
    ├── cli
    │   └── __init__.py
    ├── core
    │   └── __init__.py
    ├── data
    │   └── __init__.py
    ├── tools
    │   ├── __init__.py
    │   └── plot.py
    └── utils
        ├── __init__.py
        └── notify.py
```