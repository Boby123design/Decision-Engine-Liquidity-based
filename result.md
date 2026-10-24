# Model_7 — Live Dataset Results

## 1. Executive Summary

This report summarizes the **201 trade records** in `live_cleaned_dataset.csv`, collected from the Model_7 workflow and logged by the user after trades were taken.

| Metric | Result |
|---|---:|
| Total logged trades | **201** |
| TP outcomes | 53 (**26.37%**) |
| SL outcomes | 94 (**46.77%**) |
| CTC outcomes | 54 (**26.87%**) |
| Best setups | 73 (**36.32%** of records) |
| Good setups | 109 (**54.23%** of records) |
| Blind setups | 19 (**9.45%** of records) |
| Buy trades | 84 (**41.79%** of records) |
| Sell trades | 117 (**58.21%** of records) |

**Overall observation:** SL is the most frequently recorded outcome in this dataset. These are outcome frequencies—not a measure of Model_7's prediction accuracy or profitability.

## 2. Actual Outcome Distribution

| Recorded outcome | Number of trades | Share of all trades |
|---|---:|---:|
| TP | 53 | 26.37% |
| SL | 94 | 46.77% |
| CTC | 54 | 26.87% |
| **Total** | **201** | **100.00%** |

TP, SL, and CTC are shown exactly as they are recorded in the CSV. The file does not define the precise meaning or exit rules for CTC, so this report does not assume a particular interpretation.

## 3. Results by Setup Quality

Percentages in this table are calculated **within each setup category**, not across the entire dataset.

| Setup quality | Trades | TP | TP share | SL | SL share | CTC | CTC share |
|---|---:|---:|---:|---:|---:|---:|---:|
| Best | 73 | 26 | 35.62% | 29 | 39.73% | 18 | 24.66% |
| Good | 109 | 22 | 20.18% | 56 | 51.38% | 31 | 28.44% |
| Blind | 19 | 5 | 26.32% | 9 | 47.37% | 5 | 26.32% |

### Observations

- **Best setups had the highest observed TP share:** 26 of 73 trades (35.62%).
- **Good setups had the highest observed SL share:** 56 of 109 trades (51.38%).
- Blind setups contain only 19 records, so their percentages are based on a comparatively small sample.

These are descriptive comparisons from the logged trades. They do not establish that setup quality caused the outcomes or that the same pattern will continue in future trades.

## 4. Results by Trade Direction

Percentages are calculated within each direction.

| Direction | Trades | TP | TP share | SL | SL share | CTC | CTC share |
|---|---:|---:|---:|---:|---:|---:|---:|
| Buy | 84 | 25 | 29.76% | 33 | 39.29% | 26 | 30.95% |
| Sell | 117 | 28 | 23.93% | 61 | 52.14% | 28 | 23.93% |

### Observations

- Buy trades had a higher observed TP share than sell trades in this dataset: **29.76% vs. 23.93%**.
- Sell trades had a higher observed SL share: **52.14% vs. 39.29%**.
- More sell trades were logged than buy trades (117 vs. 84).

This comparison does not prove that buy trades are inherently better. Market conditions, asset mix, trade selection, and other factors are not recorded in the CSV and could affect the results.

## 5. Dataset Quality Checks

The supplied CSV was checked for basic completeness and category consistency.

| Check | Result |
|---|---|
| Number of rows | 201 |
| Columns present | `Image_Path`, `Trade_Type`, `Result`, `Type` |
| Missing values in these columns | 0 |
| Duplicate image paths | 0 |
| Recognized setup labels | `best`, `good`, `blind` |
| Recognized outcome labels | `tp`, `sl`, `ctc` |
| Recognized direction labels | `buy`, `sell` |

All 201 rows have a non-empty image path, setup label, outcome label, and direction label. However, the image paths are absolute Windows paths (for example, paths rooted under `C:\Models\Model_7\...`). They may not resolve on another computer unless the files are placed at the matching location or the paths are converted to project-relative paths.

## 6. What These Results Tell Us—and What They Do Not

This file is useful for describing the actual outcomes users logged after interacting with Model_7. It gives a first view of how recorded outcomes vary across setup labels and trade direction.

However, the CSV contains only four fields. It does **not** contain the model's predicted TP/SL/CTC probabilities, its AI verdict (such as SKIP), timestamps in a standardized field, asset/symbol, entry and exit prices, position size, transaction costs, or realized profit and loss.

As a result, the dataset alone cannot establish:

- Model prediction accuracy or probability calibration.
- Whether the model's SKIP verdicts were correct, because skipped opportunities are not represented here.
- Win rate under a clearly defined trading-result convention, especially while CTC is undefined.
- Net profitability, expectancy, drawdown, or risk-adjusted performance.
- Whether any observed difference is statistically reliable or will generalize to unseen trades.

**Important:** TP share is not the same as model accuracy, and outcome counts alone do not show whether the strategy made money. Profitability depends on the trade rules, reward-to-risk ratio, CTC definition, costs, and the actual monetary result of each trade.

## 7. Recommended Logging Improvements

To evaluate Model_7 rigorously, future records should link each model analysis to the corresponding executed trade and include:

1. A unique trade/analysis ID and timestamp.
2. Asset or symbol and relevant timeframe.
3. Setup quality and trade direction.
4. Predicted `P(TP)`, `P(SL)`, and `P(CTC)` captured **before** the trade outcome is known.
5. AI verdict, including `SKIP` or trade-permitted decisions.
6. Whether the user actually took the trade, so model recommendations can be evaluated separately from user selection.
7. A clearly defined CTC label and consistent outcome rules.
8. Entry, stop-loss, take-profit, exit price, position size, fees/slippage, and realized P&L where available.

With these fields, future reports can compare predictions with actual outcomes, evaluate probability calibration and decision quality, and measure trading performance using a clearly defined methodology.

---

**Source:** `live_cleaned_dataset.csv` supplied for this analysis. Counts and percentages above are calculated directly from its 201 rows. Percentages are rounded to two decimal places; small rounding differences may occur when displayed values are added together.
