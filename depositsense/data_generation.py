import numpy as np
import pandas as pd
from .config import SETTINGS

SEGMENTS = {
    "Everyday": (0.38, 0.030),
    "Savings": (0.22, 0.018),
    "Salary": (0.27, 0.024),
    "Affluent": (0.13, 0.040),
}

def generate_data(path=None, seed=SETTINGS.seed):
    """Create synthetic account/day balances and daily net outflows."""
    rng = np.random.default_rng(seed)
    n, days = SETTINGS.n_accounts, SETTINGS.n_days
    segment_names = list(SEGMENTS)
    probs = [SEGMENTS[s][0] for s in segment_names]
    segments = rng.choice(segment_names, size=n, p=probs)
    opening = rng.lognormal(mean=9.2, sigma=0.85, size=n)
    rows = []
    for account_id in range(n):
        segment = segments[account_id]
        volatility = SEGMENTS[segment][1]
        balance = opening[account_id]
        rate_sensitivity = {"Everyday": 0.20, "Savings": 0.65,
                            "Salary": 0.30, "Affluent": 0.85}[segment]
        for day in range(days):
            market_rate = 0.075 + 0.004*np.sin(2*np.pi*day/90)
            rate_gap = max(0.0, 0.085-market_rate)
            # Outflow probability responds modestly to rate competition.
            p_outflow = min(0.30, 0.035 + rate_sensitivity*rate_gap)
            material_event = rng.random() < p_outflow
            deposit = rng.lognormal(mean=5.8, sigma=0.7) if rng.random() < 0.16 else 0.0
            withdrawal = rng.lognormal(mean=5.9, sigma=0.75) if material_event else rng.lognormal(mean=4.3, sigma=0.65)
            withdrawal = min(withdrawal, balance*0.75)
            balance = max(0.0, balance + deposit - withdrawal)
            rows.append((account_id, day, segment, market_rate, deposit,
                         withdrawal, balance, int(material_event)))
    df = pd.DataFrame(rows, columns=["account_id","day","segment","market_rate",
        "deposit","withdrawal","closing_balance","material_outflow"])
    if path:
        df.to_csv(path, index=False)
    return df
