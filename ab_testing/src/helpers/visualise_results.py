import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.helpers.preprocess_data import prepare_data_for_analysis
import scipy.stats as stats
import numpy as np


def plot_conversion_rate(df):
    """
    Plot conversion rate per AB group.
    """
    conversion_rates = df.groupby('ab_group')['converted'].mean().reset_index()

    plt.figure(figsize=(8,6))
    sns.barplot(x='ab_group', y='converted', data=conversion_rates)
    plt.title('Conversion Rate by AB Group')
    plt.xlabel('AB Group')
    plt.ylabel('Conversion Rate')
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def plot_distribution(df, column='net_revenue_per_payer', group_col='ab_group'):
    groups = sorted(df[group_col].dropna().unique())
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Distribution Diagnostics for {column}", fontsize=16)

    # --- 1. Histograms ---
    for group in groups:
        sns.histplot(
            df[df[group_col] == group][column].dropna(),
            label=f'Group {group}',
            kde=True, 
            stat="density",
            bins=30,
            ax=axes[0,0],
            alpha=0.6
        )
    axes[0,0].legend()
    axes[0,0].set_title("Histogram + KDE")
    
    # --- 2. Boxplots ---
    sns.boxplot(
        x=group_col, 
        y=column, 
        data=df, 
        ax=axes[0,1],
        showfliers=True  # show outliers
    )
    axes[0,1].set_title("Boxplot")

    # --- 3. Q-Q Plots (Quantile-Quantile for Normality) ---
    for group in groups:
        stats.probplot(
            df[df[group_col] == group][column].dropna(), 
            dist="norm", 
            plot=axes[1,0]
        )
    axes[1,0].set_title("Q-Q Plot (Normality Check)")

    # --- 4. ECDFs (Empirical CDFs) ---
    for group in groups:
        subset = df[df[group_col] == group][column].dropna().sort_values()
        y = np.arange(1, len(subset)+1) / len(subset)
        axes[1,1].step(subset, y, where='post', label=f'Group {group}')
    
    axes[1,1].legend()
    axes[1,1].set_title("Empirical CDFs")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def run_all_visualizations(df):
    """
    Run all visualizations.
    """
    plot_conversion_rate(df)

    for col in ['amount_per_user', 'amount_per_payer', 'net_revenue_per_user'
                , 'net_revenue_per_payer', 'cost']:
        plot_distribution(df, col, 'ab_group')

def plot_conversion_rate_posteriors(results):
    plt.figure(figsize=(10, 6))
    palette = sns.color_palette("tab10", n_colors=len(results))
    for idx, (label, trace) in enumerate(results.items()):
        p_A_samples = trace.posterior["p_A"].values.flatten()
        p_B_samples = trace.posterior["p_B"].values.flatten()
        sns.kdeplot(p_A_samples * 100, label=f"p_A - {label}", color=palette[idx], linestyle="-")
        sns.kdeplot(p_B_samples * 100, label=f"p_B - {label}", color=palette[idx], linestyle="--")
    plt.xlabel("Conversion Rate (%)")
    plt.ylabel("Density")
    plt.title("Posterior Distributions of Conversion Rates")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_posterior_uplift_probs(results, thresholds=[0, 0.005, 0.01]):
    plt.figure(figsize=(8, 6))
    palette = sns.color_palette("tab10", n_colors=len(results))
    for idx, (label, trace) in enumerate(results.items()):
        uplift_samples = trace.posterior["uplift"].values.flatten()
        probs = [(uplift_samples > t).mean() for t in thresholds]
        plt.plot([t * 100 for t in thresholds], probs, marker="o", label=label, color=palette[idx])
    plt.xlabel("Uplift Threshold (%)")
    plt.ylabel("P(uplift > threshold)")
    plt.title("Posterior Probability That Uplift Exceeds Threshold")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_decision_boundaries(results, threshold=0.95):
    summary = []
    for label, trace in results.items():
        uplift_samples = trace.posterior["uplift"].values.flatten()
        prob = (uplift_samples > 0).mean()
        summary.append((label, prob))
    
    labels, probs = zip(*summary)
    colors = ["green" if p > threshold else "red" for p in probs]
    plt.barh(labels, probs, color=colors)
    plt.axvline(threshold, color="black", linestyle="--", label="Decision Threshold")
    plt.xlabel("P(uplift > 0)")
    plt.title("Decision Support by Prior")
    plt.grid(True, axis="x")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_cvr_posteriors_multiple(results, label_A="Group A", label_B="Group B"):
    num_priors = len(results)
    fig, axs = plt.subplots(num_priors, 1, figsize=(12.5, 4 * num_priors), constrained_layout=True)

    if num_priors == 1:
        axs = [axs]  # Ensure axs is always iterable

    for ax, (label, trace) in zip(axs, results.items()):
        samples_p_A = trace.posterior["p_A"].values.flatten()
        samples_p_B = trace.posterior["p_B"].values.flatten()

        ax.hist(samples_p_A, bins=40, density=True, alpha=0.6, label=f'Posterior of {label_A}')
        ax.hist(samples_p_B, bins=40, density=True, alpha=0.6, label=f'Posterior of {label_B}')
        ax.set_xlabel("Conversion Rate")
        ax.set_ylabel("Density")
        ax.set_title(f"{label}: Posterior Distributions of {label_A} and {label_B}")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.show()

def plot_cvr_difference_multiple(results, label_A="Group A", label_B="Group B", reference_line=None):
    num_priors = len(results)
    fig, axs = plt.subplots(num_priors, 1, figsize=(12.5, 4 * num_priors), constrained_layout=True)

    if num_priors == 1:
        axs = [axs]  # Ensure iterable if only one plot

    for ax, (label, trace) in zip(axs, results.items()):
        samples_p_A = trace.posterior["p_A"].values.flatten()
        samples_p_B = trace.posterior["p_B"].values.flatten()
        difference = samples_p_B - samples_p_A

        prob_b_better = (difference > 0).mean()

        ax.hist(difference, bins=40, density=True, alpha=0.75, color="steelblue")
        ax.axvline(0, color='black', linestyle='--')
        if reference_line is not None:
            ax.vlines(reference_line, 0, ax.get_ylim()[1], linestyle='--', color='red',
                      label=f'Reference = {reference_line:.2%}')
        ax.set_xlabel(f"Conversion Rate Difference: {label_B} - {label_A}")
        ax.set_ylabel("Density")
        ax.set_title(f"{label}: Posterior Distribution of Conversion Rate Difference")

        # Annotate with probability
        ax.text(0.95, 0.90,
                f"P({label_B} > {label_A}) = {prob_b_better:.3f}",
                transform=ax.transAxes,
                ha='right',
                fontsize=11,
                bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))

        if reference_line is not None:
            ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.show()



if __name__ == "__main__":
    run_all_visualizations()
