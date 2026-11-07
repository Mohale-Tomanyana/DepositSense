from pathlib import Path
import numpy as np
import pandas as pd
from depositsense.config import SETTINGS
from depositsense.data_generation import generate_data
from depositsense.analysis import (segment_summary, confidence_interval,
    bootstrap_mean_interval, least_squares_trend, buffer_cost, marginal_holding_cost)
from depositsense.bayes import beta_binomial_update
from depositsense.simulation import simulate_net_outflows
from depositsense.reporting import create_outputs

ROOT = Path(__file__).resolve().parent
DATA = ROOT/"data"/"account_daily.csv"
OUTPUTS = ROOT/"outputs"

def main():
    df = generate_data(DATA)
    summary = segment_summary(df)
    daily = (df.groupby("day")
             .agg(deposits=("deposit","sum"), withdrawals=("withdrawal","sum"))
             .reset_index())
    daily["net_outflow"] = daily["withdrawals"]-daily["deposits"]

    # Use the first half to establish an account-level material-outflow threshold;
    # estimate event frequency on the second half to avoid using the same observations
    # to define and estimate the event.
    first_half = df[df.day < SETTINGS.n_days//2]
    thresholds = first_half.groupby("account_id")["withdrawal"].quantile(0.90)
    second_half = df[df.day >= SETTINGS.n_days//2].copy()
    second_half["material_event"] = [
        int(w > thresholds.loc[a]) for a,w in
        zip(second_half.account_id, second_half.withdrawal)
    ]
    bayes = beta_binomial_update(second_half["material_event"],
        SETTINGS.prior_alpha, SETTINGS.prior_beta)

    ci = confidence_interval(daily["net_outflow"])
    boot = bootstrap_mean_interval(daily["net_outflow"])
    intercept, slope = least_squares_trend(daily["net_outflow"])

    baseline = simulate_net_outflows(daily["net_outflow"], stress=False)
    stress = simulate_net_outflows(daily["net_outflow"], stress=True)
    policies = []
    for q in SETTINGS.buffer_quantiles:
        buffer = float(np.quantile(stress, q))
        policies.append((q, buffer, buffer_cost(buffer, stress)))

    print("\nDEPOSITSENSE | RETAIL DEPOSIT STABILITY & LIQUIDITY")
    print("\nSEGMENT SUMMARY")
    print(summary.round(2).to_string(index=False))
    print(f"\nAverage daily net outflow: {daily.net_outflow.mean():,.2f}")
    print(f"95% confidence interval: ({ci[0]:,.2f}, {ci[1]:,.2f})")
    print(f"Bootstrap 95% interval: ({boot[0]:,.2f}, {boot[1]:,.2f})")
    print(f"Bayesian posterior mean material-outflow probability: {bayes['posterior_mean']:.3%}")
    print(f"Approximate 95% posterior interval: {bayes['approx_95_interval']}")
    print(f"Least-squares trend slope: {slope:,.2f} currency units/day")
    print(f"Marginal holding cost rate: {marginal_holding_cost(1_000_000):.4f}")
    print("\nSTRESS-SCENARIO BUFFER POLICIES")
    for q, buffer, cost in policies:
        print(f"{q:.0%} percentile: buffer={buffer:,.2f}, expected cost={cost:,.2f}")

    create_outputs(daily, summary, policies, OUTPUTS/"depositsense_report.txt", OUTPUTS)
    print(f"\nReport and charts saved to: {OUTPUTS}")

if __name__ == "__main__":
    main()
