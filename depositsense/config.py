from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    seed: int = 20261108
    n_accounts: int = 1800
    n_days: int = 180
    simulation_days: int = 30
    bootstrap_samples: int = 1000
    prior_alpha: float = 2.0
    prior_beta: float = 8.0
    material_outflow_threshold: float = 0.10
    stress_multiplier: float = 1.55
    funding_shortfall_cost: float = 0.06
    liquidity_holding_cost: float = 0.0015
    buffer_quantiles: tuple = (0.80, 0.90, 0.95)

SETTINGS = Settings()
