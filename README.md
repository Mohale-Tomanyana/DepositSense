# DepositSense
## Retail Deposit Stability & Liquidity Risk Analytics

**DepositSense** is an educational banking analytics project that helps a bank understand how stable its retail deposit funding is and how much liquidity it may need under changing customer behaviour and interest-rate conditions.

A bank cannot assume that every rand deposited by customers will remain in their accounts. Customers may withdraw funds, transfer money, or move savings when competing banks offer better rates. DepositSense studies those behaviours using simulated account-level data, statistical inference, Bayesian updating and Monte Carlo scenario analysis.

### The banking question

> How much of our retail deposit base can we reasonably treat as stable, and what liquidity buffer should we prepare if withdrawals increase?

### What it does

1. Generates synthetic daily account-balance observations for several customer segments.
2. Measures balance stability, withdrawal rates and deposit concentration.
3. Estimates uncertainty around average daily outflows using confidence intervals and bootstrap resampling.
4. Uses a Beta-Binomial model to update the probability that an account experiences a material outflow.
5. Fits a simple least-squares trend to aggregate deposits.
6. Simulates 30-day net deposit outflows under baseline and stress scenarios.
7. Compares liquidity buffers and their illustrative funding/holding costs.
8. Produces charts and a plain-text management report.

### Statistical methods

- **Descriptive statistics:** mean, median, standard deviation, quantiles and segment summaries.
- **Probability and distributions:** Bernoulli event indicators, binomial sampling and empirical resampling.
- **Statistical inference:** normal-approximation confidence interval and bootstrap interval.
- **Bayesian inference:** Beta prior updated with observed material-outflow events.
- **Mathematical modelling:** liquidity-buffer cost function.
- **Linear algebra:** least-squares trend estimated with `numpy.linalg.lstsq`.
- **Monte Carlo simulation:** future net outflow scenarios.
- **OOP/software design:** dataclasses and separated modules.

### Data and limitations

All data is synthetic. It is not customer data and does not represent any real bank. Interest-rate sensitivity and stress multipliers are illustrative assumptions, not calibrated forecasts. The project is a learning prototype, not a regulatory liquidity model or a production banking system. A real deployment would require validated bank data, governance, model-risk review and regulatory alignment.

### Run it

```bash
python -m pip install -r requirements.txt
python main.py
```

Run the tests:

```bash
python -m unittest discover -s tests -v
```

Outputs are saved in `outputs/`.

### Project structure

```text
DepositSense/
├── depositsense/
│   ├── config.py
│   ├── data_generation.py
│   ├── analysis.py
│   ├── bayes.py
│   ├── simulation.py
│   └── reporting.py
├── data/
├── outputs/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```
## Project Visualisation

### Liquidity Buffer Comparison

![DepositSense Liquidity Policy Costs](outputs/liquidity_policy_costs.png)

---

**Copyright © 2026 Mohale Tomanyana. All rights reserved.**

This project was developed by Mohale Tomanyana for educational and portfolio purposes.
