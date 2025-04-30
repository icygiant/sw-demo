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

if __name__ == "__main__":
    run_all_visualizations()
