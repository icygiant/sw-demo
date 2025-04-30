import pandas as pd

def load_data(file_path):
    """
    Loads the csv data into a pandas dataframe.
    """
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    """
    Preprocesses the data:
    - Handles necessary type casts
    - Handles missing values
    - Creates a binary conversion metric
    - Creates "amount per user"
    - Creates "net revenue per user"
    - Creates "net revenue per payer"

    """
    df = df.copy()
    
    # Convert timestamps to datetime
    df['install_time'] = pd.to_datetime(df['install_time'], errors='coerce')
    df['payment_time'] = pd.to_datetime(df['payment_time'], errors='coerce')
    

    # Impute (potentially) missing costs with the median value
    df['cost'] = df['cost'].fillna(df['cost'].median())

    # Create the binary conversion metric: 1 if payment made, 0 if not
    df['converted'] = df['payment_time'].notna().astype(int)

    # "Create" amount per payer
    df = df.rename(columns={'amount': 'amount_per_payer'})

    # Impute missing payment amounts with 0 to create amount per user
    df['amount_per_user'] = df['amount_per_payer'].fillna(0)

    # Create net revenue per user (amount per user - cost)
    df['net_revenue_per_user'] = df['amount_per_user'] - df['cost']

    # Create net revenue per payer (amount per payer - cost)
    df['net_revenue_per_payer'] = (df['amount_per_payer'] - df['cost'])
    

    return df

def create_summary_metrics(df):
    """
    Creates aggregated metrics per A/B group.
    Returns a summary dataframe.
    """
    summary = df.groupby('ab_group').agg(
        users=('user_id', 'count'),
        converters=('converted', 'sum'),
        conversion_rate=('converted', 'mean'),
        avg_amount_per_user=('amount_per_user', 'mean'),
        avg_amount_per_payer=('amount_per_payer', 'mean'),
        avg_net_revenue_per_user=('net_revenue_per_user', 'mean'),
        avg_net_revenue_per_payer=('net_revenue_per_payer', 'mean')
    ).reset_index()

    # Calculate conversion rate uplift from group 1 to group 2
    summary['cvr_uplift'] = 100 * (
        (summary['conversion_rate'] / summary.loc[summary['ab_group'] == 1, 'conversion_rate'].values[0]) - 1
    )
    
    return summary

def prepare_data_for_analysis(file_path):
    """
    The full pipeline to load, preprocess, and summarize the data.
    """
    df = load_data(file_path)
    df = preprocess_data(df)
    summary = create_summary_metrics(df)
    
    return df, summary

def preaggregate_data_for_analysis(file_path, col):
    _, sum_df = prepare_data_for_analysis(file_path)
    df = sum_df[['ab_group', 'users', col]]
    return df

if __name__ == "__main__":
    _df, summary_metrics = prepare_data_for_analysis()
