import numpy as np

def beta_binomial_update(events, alpha=2.0, beta=8.0):
    """Posterior for the probability of a material-outflow day."""
    x = np.asarray(events, dtype=int)
    successes = int(x.sum())
    failures = int(len(x)-successes)
    a_post, b_post = alpha+successes, beta+failures
    mean = a_post/(a_post+b_post)
    variance = a_post*b_post/((a_post+b_post)**2*(a_post+b_post+1))
    sd = np.sqrt(variance)
    # Normal approximation is reported explicitly; Beta quantiles are not implied.
    interval = (max(0.0, mean-1.96*sd), min(1.0, mean+1.96*sd))
    return {"prior_alpha": alpha, "prior_beta": beta,
            "events": successes, "non_events": failures,
            "posterior_alpha": a_post, "posterior_beta": b_post,
            "posterior_mean": float(mean),
            "approx_95_interval": tuple(map(float, interval))}
