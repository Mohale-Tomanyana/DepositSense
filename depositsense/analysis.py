import numpy as np
from statistics import NormalDist
from .config import SETTINGS

def segment_summary(df):
    return (df.groupby("segment")
            .agg(accounts=("account_id","nunique"),
                 average_balance=("closing_balance","mean"),
                 median_balance=("closing_balance","median"),
                 balance_std=("closing_balance","std"),
                 total_deposits=("deposit","sum"),
                 total_withdrawals=("withdrawal","sum"),
                 material_outflow_rate=("material_outflow","mean"))
            .reset_index())

def confidence_interval(values, confidence=0.95):
    x = np.asarray(values, dtype=float)
    mean = float(x.mean())
    se = float(x.std(ddof=1)/np.sqrt(len(x)))
    z = NormalDist().inv_cdf(0.5+confidence/2)
    return mean-z*se, mean+z*se

def bootstrap_mean_interval(values, samples=SETTINGS.bootstrap_samples, seed=SETTINGS.seed):
    x = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = np.array([rng.choice(x, size=len(x), replace=True).mean() for _ in range(samples)])
    return tuple(np.quantile(means, [0.025, 0.975]))

def least_squares_trend(series):
    y = np.asarray(series, dtype=float)
    x = np.arange(len(y), dtype=float)
    design = np.column_stack([np.ones(len(x)), x])
    intercept, slope = np.linalg.lstsq(design, y, rcond=None)[0]
    return float(intercept), float(slope)

def buffer_cost(buffer_amount, simulated_outflows):
    """Illustrative expected cost: shortage cost plus liquidity holding cost."""
    outflows = np.asarray(simulated_outflows, dtype=float)
    shortfall = np.maximum(outflows-buffer_amount, 0.0)
    excess = np.maximum(buffer_amount-outflows, 0.0)
    return float(SETTINGS.funding_shortfall_cost*shortfall.mean()
                 + SETTINGS.liquidity_holding_cost*excess.mean())

def marginal_holding_cost(buffer_amount):
    """Derivative of the linear holding-cost component with respect to buffer."""
    return SETTINGS.liquidity_holding_cost
