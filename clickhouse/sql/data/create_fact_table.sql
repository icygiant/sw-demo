create table if not exists sw_test.fact_table
(
    user_id UInt64,
    event_name LowCardinality(String),
    event_time DateTime,
    currency LowCardinality(Nullable(String)),
    amount Decimal(10, 2),
    ingest_time DateTime DEFAULT now(),
    
    event_id UInt64 MATERIALIZED
        sipHash64(toString(user_id) || toString(toUnixTimestamp(event_time)) || event_name)
)
ENGINE = ReplacingMergeTree(ingest_time)
partition by (event_name) -- low-cardinality (at least for now)
order by (event_id)
SETTINGS index_granularity = 8192;
