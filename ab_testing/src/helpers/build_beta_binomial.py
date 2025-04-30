import pymc as pm
import arviz as az
import numpy as np
from contextlib import redirect_stdout
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display


def run_beta_binomial_model(data, prior_alpha, prior_beta, seed=42):
    with pm.Model() as model:
        # Priors for conversion rates
        p_A = pm.Beta("p_A", alpha=prior_alpha, beta=prior_beta)
        p_B = pm.Beta("p_B", alpha=prior_alpha, beta=prior_beta)

        # Uplift
        uplift = pm.Deterministic("uplift", (p_B - p_A) / p_A)

        # Likelihood
        pm.Binomial("obs_A", n=data['users'][0], p=p_A, observed=data['converters'][0])
        pm.Binomial("obs_B", n=data['users'][1], p=p_B, observed=data['converters'][1])

        # Sampling
        trace = pm.sample(5000, tune=1000, target_accept=0.95,
                          chains=4,
                          random_seed=seed,
                          return_inferencedata=True,
                          progressbar=False)  # Turn off the progress bar

    return trace

def run_sensitivity_analysis(data, priors):
    results = {}
    for label, (alpha, beta) in priors.items():
        f = io.StringIO()
        with redirect_stdout(f):  # Silences print output from PyMC internals
            trace = run_beta_binomial_model(data, alpha, beta)
        results[label] = trace
    return results

def summarize_posteriors(results):
    summary = []
    for label, trace in results.items():
        uplift_samples = trace.posterior["uplift"].values.flatten()
        prob_positive = (uplift_samples > 0).mean()
        mean_uplift = uplift_samples.mean()
        ci_lower, ci_upper = np.percentile(uplift_samples, [2.5, 97.5])
        summary.append({
            "Prior": label,
            "Mean uplift (%)": mean_uplift * 100,
            "95% CI (%)": f"[{ci_lower*100:.2f}, {ci_upper*100:.2f}]",
            "P(uplift > 0)": prob_positive
        })
    return pd.DataFrame(summary)