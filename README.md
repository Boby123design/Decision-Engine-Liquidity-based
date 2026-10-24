# Model_7 — Multi-Modal Scalping Terminal

A Windows-based Streamlit research prototype that analyzes a trading-chart snapshot with a PyTorch model, displays estimated **TP / SL / CTC** probabilities, and lets the user log the trade's actual outcome for later analysis.

> **Risk notice:** This is an experimental decision-support tool, not a guarantee of profitable trades or financial advice. Validate it out-of-sample and account for execution costs before relying on its output.

## How it works

1. Run `run_model7.bat`.
2. Capture a chart automatically, paste it, or upload an image.
3. Select setup quality (`Blind`, `Good`, `Best`) and direction (`Buy`, `Sell`).
4. Click **Analyze Probability** to see TP, SL, and CTC estimates and the app's `SKIP` / `CAUTION` / `ENTRY` verdict.
5. After the trade, select its actual outcome and save the record to `live_cleaned_dataset.csv`.

![Model_7 terminal](screenshots/02-terminal-home.png)

![AI verdict](screenshots/04-ai-verdict.png)

## Model

- **Image branch:** ResNet-18 CNN, resized to 224 × 224.
- **Tabular branch:** setup quality and trade direction.
- **Fusion classifier:** combines both branches to estimate three classes: `CTC`, `SL`, and `TP`.
- **Inference weights:** `forex_model.pth`.

The app's current verdict thresholds are rule-based on the model's estimated probabilities; they should not be interpreted as validated trading performance.

## Run locally (Windows)

Requires Python and the model weights. In a terminal at the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install streamlit torch torchvision pandas pillow pywin32 openpyxl scikit-learn
python -m streamlit run app_model7.py --server.port 8507
```

You can also double-click `run_model7.bat`. Automatic chart capture uses Windows-specific screen/window APIs and fixed screen coordinates; these may need adjustment on another display. The current scripts also contain local Windows paths (`C:\Models\Model_7`) that may need changing on another machine.

## Recorded live results

The supplied `live_cleaned_dataset.csv` contains **201 logged outcomes**: **53 TP (26.37%)**, **94 SL (46.77%)**, and **54 CTC (26.87%)**. These are outcome frequencies—not model accuracy, probability calibration, or proof of profitability. The current CSV does not store the prediction probabilities or AI verdict alongside each result.

See [result.md](result.md) for the dataset breakdown and [working.md](working.md) for the user workflow.

## Main files

| File | Purpose |
|---|---|
| `app_model7.py` | Streamlit app, inference, verdict, and live-outcome logging |
| `model_architecture.py` | Multi-modal PyTorch model |
| `train_model.py` | Training script |
| `dataset_loader.py` | Image/tabular dataset loader |
| `forex_model.pth` | Saved model weights |
| `live_cleaned_dataset.csv` | User-logged live outcomes |
| `working.md` / `result.md` | Workflow guide / dataset analysis |

## Data and security

Never commit broker passwords, API keys, tokens, account identifiers, or personal data. Review chart screenshots and datasets before publishing. Keep private model weights, trade images, or training data out of a public repository if they contain proprietary strategy information. Add sensitive/local files to `.gitignore`; this does not remove copies already committed to Git history. If a credential was exposed, revoke or rotate it immediately.
