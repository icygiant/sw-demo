create table sw_test.fact_with_eur_conversions (
    user_id UInt64,
    event_name LowCardinality(String),
    event_time DateTime,
    currency LowCardinality(Nullable(String)),
    amount Decimal(10, 2),
    amount_in_eur Decimal(10, 2)
)
engine = MergeTree() order by (event_id)
partition by toYYYYMM(event_time);

--  create a materialized view to combine exchange rates and transaction data
create materialized view sw_test.mvw_fact_with_eur_conversions to sw_test.fact_with_eur_conversions
as
select
    f.event_id
    , f.user_id
    , f.amount
    , f.event_time
    , f.currency
    , coalesce(f.amount * er.rate_to_eur, f.amount) as amount_in_eur
    , f.event_name
from
    sw_test.fact_table f
left join
    sw_test.exchange_rates er
    on lower(f.currency) = er.currency_code
    and toDate(f.event_time) = er.rate_date
where
    lower(f.event_name) = 'payment';
