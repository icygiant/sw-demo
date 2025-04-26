create table if not exists main.fact_table
(
    user_id UInt64,
    event_name String,
    event_time DateTime,
    currency Nullable(String),
    amount Nullable(Float32)
)
engine = MergeTree
partition by toYYYYMM(event_time)  -- partition data by month for better manageability
order by (event_time, user_id)              -- primary sorting order
sample by user_id                  -- optional, useful for large datasets with sampling queries, not really relevant for such a smol demo :D
settings index_granularity = 8192;  -- fine-tuning the granularity for optimal performance
