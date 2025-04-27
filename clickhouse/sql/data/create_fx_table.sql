-- create the exchange_rates table in clickhouse
create table if not exists sw_test.exchange_rates
(
    currency_code lowCardinality(String),  -- lowCardinality for currency codes, as they are usually repeated
    rate_to_eur Float64,  -- use Float64 for high precision with currency rates
    rate_date Date
)
engine = ReplacingMergeTree()
partition by toYYYYMM(rate_date)
order by (currency_code, rate_date);
