from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def create_outputs(daily, summary, policies, report_path, output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9,5))
    ax.bar(summary["segment"], summary["average_balance"])
    ax.set(title="Average account balance by customer segment",
           xlabel="Customer segment", ylabel="Average closing balance")
    fig.tight_layout()
    fig.savefig(out/"deposit_balances_by_segment.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8,5))
    labels = [f"{int(q*100)}th percentile" for q,_,_ in policies]
    costs = [cost for _,_,cost in policies]
    ax.bar(labels, costs)
    ax.set(title="Illustrative liquidity-buffer policy costs",
           ylabel="Expected cost (model units)")
    fig.tight_layout()
    fig.savefig(out/"liquidity_policy_costs.png", dpi=150)
    plt.close(fig)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("DEPOSITSENSE — MANAGEMENT SUMMARY\n")
        f.write("Synthetic educational analysis; not a bank forecast.\n\n")
        f.write(summary.to_string(index=False))
        f.write("\n\nLIQUIDITY BUFFER POLICIES\n")
        for q, buffer, cost in policies:
            f.write(f"{q:.0%} buffer: {buffer:,.2f} | expected cost: {cost:,.2f}\n")
