import numpy as np
from .config import SETTINGS

def simulate_net_outflows(daily_net_outflow, n_sims=5000, horizon=SETTINGS.simulation_days,
                          stress=False, seed=SETTINGS.seed):
    """Bootstrap daily net outflows into future horizons."""
    history = np.asarray(daily_net_outflow, dtype=float)
    rng = np.random.default_rng(seed + (1 if stress else 0))
    draws = rng.choice(history, size=(n_sims, horizon), replace=True)
    if stress:
        # Stress case: larger outflows and reduced inflows, represented by a transparent multiplier.
        draws = np.where(draws > 0, draws*SETTINGS.stress_multiplier, draws*0.85)
    return draws.sum(axis=1)
