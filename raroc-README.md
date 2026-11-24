# RAROC Calculator

> An interactive Streamlit app that calculates **Risk-Adjusted Return on Capital (RAROC)** so credit pricing and capital-allocation decisions account for risk, not just revenue.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-FF4B4B)
![Tests](https://img.shields.io/badge/tests-pytest-green)

<!-- Add a screenshot: save it as docs/screenshot.png, then uncomment the line below -->
<!-- ![App screenshot](docs/screenshot.png) -->

## 🎯 The Problem

Profitability measures like ROA or net interest margin treat a safe loan and a risky loan with the same yield as equally attractive. They aren't: the risky one consumes more capital and is more likely to produce losses. Banks need a metric that compares returns **after** adjusting for expected losses and the capital held against unexpected ones.

## 💡 The Solution

This calculator computes RAROC for a loan or portfolio segment and compares it against a hurdle rate, so a user can see quickly whether a deal creates value for the bank.

```
RAROC = (Revenue − Operating Costs − Expected Loss) / Economic Capital
```

| Component | Meaning |
|---|---|
| **Revenue** | Interest income plus fees, net of cost of funds |
| **Operating Costs** | Cost of servicing and administering the exposure |
| **Expected Loss (EL)** | PD × LGD × EAD |
| **Economic Capital** | Capital held against unexpected losses |

> ⚠️ *Check this section against `risk_engine.py` and edit it so it matches exactly what your code calculates (for example, tax treatment or a capital-benefit term).*

## ✨ Features

- Interactive inputs in the browser (no code needed)
- Calculates expected loss, risk-adjusted return and RAROC %
- Compares RAROC with a hurdle rate to give a clear pass/fail signal
- Unit-tested calculation engine, separated from the UI

## 🚀 Quick Start

```bash
git clone https://github.com/chandrasekhar-runku/raroc-calculator.git
cd raroc-calculator
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## 🧮 Worked Example

*Illustrative numbers only. Update these to match your app's actual inputs and output.*

| Input | Value |
|---|---|
| Exposure at default (EAD) | ₹10,00,00,000 |
| Revenue (net of funding cost) | ₹90,00,000 |
| Operating cost | ₹15,00,000 |
| PD / LGD | 1.5% / 45% |
| Economic capital | ₹80,00,000 |

- Expected loss = 1.5% × 45% × ₹10 Cr = **₹6,75,000**
- RAROC = (90,00,000 − 15,00,000 − 6,75,000) / 80,00,000 = **85.3%**

## 🏗️ Project Structure

```
raroc-calculator/
├── app.py                 # Streamlit user interface
├── risk_engine.py         # RAROC and expected-loss calculation logic
├── test_risk_engine.py    # Unit tests for the calculation engine
└── requirements.txt       # Python dependencies
```

The calculation logic is kept separate from the UI, which makes it testable and reusable in other tools.

## 🧪 Testing

```bash
pip install pytest
pytest -v
```

## 🛠️ Tech Stack

Python · Streamlit · pytest

## ⚠️ Disclaimer

This project is for educational and portfolio purposes. It uses illustrative inputs and generic assumptions and contains no client or employer data. It is not financial advice or a production risk model.

## 👤 Author

**Chandrasekhar Runku**: IIM Ranchi MBA (Finance) · PMP® · Credit & Risk Analytics
[LinkedIn](https://linkedin.com/in/chandrasekharrunku)
