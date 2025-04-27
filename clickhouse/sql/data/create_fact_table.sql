create table if not exists sw_test.fact_table
(
    user_id UInt64,
    event_name LowCardinality(String),
    event_time DateTime,
    currency LowCardinality(Nullable(String)),
    amount Nullable(Float32)
    
    --INDEX idx_currency currency TYPE set(100) GRANULARITY 1
    --INDEX idx_event_name event_name TYPE set(100) GRANULARITY 1
)

engine = MergeTree
partition by (event_name)
order by (event_time, user_id)
sample by user_id -- optional, useful for large datasets with sampling queries, not really relevant for such a smol demo :D
settings index_granularity = 8192; -- fine-tuning the granularity for optimal performance
