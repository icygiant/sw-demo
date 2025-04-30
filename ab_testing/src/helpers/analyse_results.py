# Imports
import pandas as pd
from scipy import stats
import numpy as np
from IPython.display import display, Markdown
from src.helpers.preprocess_data import prepare_data_for_analysis

# Compare conversion rates
def compare_conversions(df):
    """
    Compare conversion rates between groups using:
    - Fisher's Exact Test
    - Chi-squared Test
    """
    contingency = pd.crosstab(df['ab_group'], df['converted'])

    if contingency.shape == (2, 2):
        fisher_oddsratio, fisher_p = stats.fisher_exact(contingency)
    else:
        fisher_oddsratio, fisher_p = np.nan, np.nan

    chi2_stat, chi2_p, chi2_dof, chi2_expected = stats.chi2_contingency(contingency)

    results = {
        "Fisher's Exact Test p-value": fisher_p,
        "Chi-Squared Test p-value": chi2_p
    }
    return results

# Compare continuous metrics
def compare_continuous(df, metric_col):
    """
    Compare continuous metrics between groups using:
    - Z-test (approximate)
    - Student's t-test (equal variances)
    - Welch's t-test (unequal variances)
    - Mann-Whitney U test (non-parametric)
    """
    group1 = df[df['ab_group'] == 1][metric_col].dropna()
    group2 = df[df['ab_group'] == 2][metric_col].dropna()

    n1, n2 = len(group1), len(group2)
    mean1, mean2 = group1.mean(), group2.mean()
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_se = np.sqrt(var1/n1 + var2/n2)
    z_stat = (mean1 - mean2) / pooled_se
    z_p = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    t_stat_student, t_p_student = stats.ttest_ind(group1, group2, equal_var=True)
    t_stat_welch, t_p_welch = stats.ttest_ind(group1, group2, equal_var=False)
    u_stat, u_p = stats.mannwhitneyu(group1, group2, alternative='two-sided')

    results = {
        "Z-test p-value": z_p,
        "Student's t-test p-value": t_p_student,
        "Welch's t-test p-value": t_p_welch,
        "Mann-Whitney U test p-value": u_p
    }
    return results

# Run full comparison
def run_full_comparison(df):
    """
    Run the full comparison across binary and continuous metrics with nicely formatted output.
    """
    # Binary Metrics
    display(Markdown("## 📊 Binary Metric: Conversion Rate Comparison"))
    conv_results = compare_conversions(df)
    conv_table = pd.DataFrame(conv_results.items(), columns=["Test", "p-value"])
    display(conv_table.style.format({"p-value": "{:.5f}"}))

    # Continuous Metrics
    display(Markdown("## 📈 Continuous Metrics Comparison"))
    continuous_metrics = ['amount_per_user', 'amount_per_payer', 'net_revenue_per_user', 'net_revenue_per_payer']
    
    for metric in continuous_metrics:
        display(Markdown(f"### ➡️ Metric: `{metric}`"))
        cont_results = compare_continuous(df, metric)
        cont_table = pd.DataFrame(cont_results.items(), columns=["Test", "p-value"])
        display(cont_table.style.format({"p-value": "{:.5f}"}))


if __name__ == "__main__":
    run_full_comparison()