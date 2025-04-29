-- so I can use sumMerge() later when querying total_amount_eur and uniqMerge() when querying event_count
create table sw_test.user_daily_history(
    user_id UInt64,
    event_date Date,
    event_name LowCardinality(String),
    event_count AggregateFunction(uniq, Nullable(Int32)), 
    total_amount_eur AggregateFunction(sum, Nullable(Int32))
)
engine = AggregatingMergeTree() order by (user_id, event_date, event_name);

create materialized view sw_test.mvw_user_daily_history to sw_test.user_daily_history
as
select
    f.user_id
    , ToDate(f.event_time) as event_date
    , f.event_name
    , uniqState(f.event_id) as event_count
    , sumState(coalesce(mv.amount_in_eur, 0)) as total_amount_eur
from sw_test.fact_table f
left join sw_test.mvw_fact_with_eur_conversions mv
group by 1,2,3;