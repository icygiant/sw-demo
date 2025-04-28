# 📦 Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Markdown
from datetime import datetime
from preprocess_data import prepare_data_for_analysis

# 📋 Helper: Section Header
def section_header(text):
    display(Markdown(f"## {text}"))

# 📋 Helper: Highlight Outliers
def highlight_outliers(df, col):
    z_scores = (df[col] - df[col].mean()) / df[col].std()
    outliers = df[abs(z_scores) > 3]
    if not outliers.empty:
        display(Markdown(f"#### Outliers detected in `{col}`"))
        display(outliers)
    else:
        display(Markdown(f"#### No significant outliers in `{col}`"))

# 🔎 Basic Data Overview
def data_overview(df):
    section_header("🔎 Basic Data Overview")
    
    section_header("Missing Values")
    display(df.isnull().sum())
    
    section_header("Data Types")
    display(df.dtypes)
    
    section_header("Summary Statistics by AB Group")
    display(df.groupby('ab_group').agg({
        'converted': ['mean', 'sum', 'count'],
        'amount_per_user': ['mean', 'std', 'median'],
        'amount_per_payer': ['mean', 'std', 'median'],
        'net_revenue_per_user': ['mean', 'std', 'median'],
        'net_revenue_per_payer': ['mean', 'std', 'median'],
        'cost': ['mean', 'std', 'median']
    }))

# 📊 Check Numerical Anomalies
def check_numerical_anomalies(df):
    section_header("📊 Checking Numerical Anomalies")
    
    numerical_cols = ['amount_per_user', 'amount_per_payer', 'cost']
    
    for col in numerical_cols:
        highlight_outliers(df, col)
    
    # 📈 Histograms
    df[numerical_cols].hist(bins=20, figsize=(12, 6))
    plt.suptitle("Histograms of Numerical Columns", fontsize=16)
    plt.tight_layout()
    plt.show()

# 🕒 Check Date/Time Anomalies
def check_datetime_anomalies(df):
    section_header("🕒 Checking Date/Time Anomalies")
    
    df['install_time'] = pd.to_datetime(df['install_time'], errors='coerce')
    df['payment_time'] = pd.to_datetime(df['payment_time'], errors='coerce')
    
    section_header("Install Time Range")
    print(f"Min: {df['install_time'].min()}, Max: {df['install_time'].max()}")
    
    # Payments before install?
    df['payment_time_before_install'] = df['payment_time'] < df['install_time']
    payment_before_install = df[df['payment_time_before_install'] == True]
    
    if not payment_before_install.empty:
        section_header("⚠️ Payments Before Installation Detected")
        display(payment_before_install)
    else:
        section_header("✅ No Payments Before Install Detected")

# 🧹 Check Missing Data
def check_missing_data(df):
    section_header("🧹 Checking Missing Data in Critical Columns")
    
    critical_cols = ['install_time', 'payment_time', 'amount_per_payer', 'cost']
    missing_data = df[critical_cols].isnull().sum().sort_values(ascending=False)
    display(missing_data)
    
    # Heatmap
    plt.figure(figsize=(10, 5))
    sns.heatmap(df[critical_cols].isnull(), cbar=False, cmap='viridis', yticklabels=False)
    plt.title("Missing Data Heatmap", fontsize=16)
    plt.tight_layout()
    plt.show()

# 🧪 Check AB Group Anomalies
def check_ab_group_anomalies(df):
    section_header("🧪 Checking AB Group Anomalies")
    
    ab_group_counts = df['ab_group'].value_counts()
    display(ab_group_counts)
    
    # Unexpected Groups
    unexpected_groups = df[~df['ab_group'].isin([1, 2])]
    if not unexpected_groups.empty:
        section_header("⚠️ Unexpected Groups Detected")
        display(unexpected_groups)
    else:
        section_header("✅ No Unexpected Groups Detected")

# 🔥 Full EDA Pipeline
def perform_eda(file_path):
    section_header("🔥 Performing Full EDA")
    
    # Load Data
    df, _ = prepare_data_for_analysis(file_path)
    
    # Overview
    data_overview(df)
    
    # Numerical Anomalies
    check_numerical_anomalies(df)
    
    # Datetime Anomalies
    check_datetime_anomalies(df)
    
    # Missing Data
    check_missing_data(df)
    
    # AB Group Anomalies
    check_ab_group_anomalies(df)


if __name__ == "__main__":
    perform_eda()
