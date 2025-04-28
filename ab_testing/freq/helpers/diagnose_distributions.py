# Imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, normaltest, skew, kurtosis
from IPython.display import display, Markdown

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 5)

# Helper: Section Header
def section_header(text):
    display(Markdown(f"## {text}"))

# Main: Diagnose Distribution
def diagnose_distribution(df, column, group_col='ab_group', filter_fn=None):
    section_header(f"🔍 Diagnostics for `{column}`")
    
    for group in sorted(df[group_col].dropna().unique()):
        # Filter
        condition = (df[group_col] == group)
        if filter_fn:
            condition &= filter_fn(df[column])
        subset = df.loc[condition, column].dropna()
        
        # Summary Table
        summary = pd.DataFrame({
            "Group": [group],
            "n": [len(subset)],
            "Mean": [subset.mean()],
            "Median": [subset.median()],
            "Std": [subset.std()],
            "Skewness": [skew(subset)],
            "Kurtosis": [kurtosis(subset)]
        })
        # Only format numeric columns
        numeric_cols = ["Mean", "Median", "Std", "Skewness", "Kurtosis"]
        display(summary.style.format({col: "{:.2f}" for col in numeric_cols}))
        
        # Normality Tests
        normality_results = []
        if 3 <= len(subset) <= 5000:
            _, p_shapiro = shapiro(subset)
            normality_results.append(("Shapiro-Wilk", p_shapiro))
        else:
            normality_results.append(("Shapiro-Wilk (Skipped)", np.nan))
        
        _, p_dagostino = normaltest(subset)
        normality_results.append(("D’Agostino’s K²", p_dagostino))
        
        norm_df = pd.DataFrame(normality_results, columns=["Test", "p-value"])
        display(norm_df.style.format({"p-value": "{:.4f}"}))
        
        # Plot
        sns.histplot(subset, kde=True, stat="density", label=f"Group {group}", bins=30, alpha=0.6)
    
    plt.title(f"Distribution of `{column}` by Group")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Diagnose relevant variables
def diagnose_relevant_variables(df):
    cols = ['amount_per_user', 'amount_per_payer', 'net_revenue_per_user',
            'net_revenue_per_payer', 'cost']
    for col in cols:
        diagnose_distribution(df, col)

if __name__ == "__main__":
    diagnose_relevant_variables()