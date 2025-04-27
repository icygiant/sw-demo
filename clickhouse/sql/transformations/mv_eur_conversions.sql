-- step 1: create a materialized view to pre-aggregate exchange rates and transaction data
create materialized view if not exists sw_test.mvw_fact_with_conversions
engine = MergeTree()
partition by toYYYYMM(event_time)  -- partitioning by month for efficient time-based queries
order by (user_id, event_time)  -- ordering by user_id and event_time for optimized query performance
as
select
    f.user_id,
    f.amount,
    f.event_time,
    f.currency,
    -- convert non-eur currencies using exchange rate, fall back to amount if no rate available
    coalesce(f.amount * er.rate_to_eur, f.amount) as amount_in_eur,
    f.event_name
from
    sw_test.fact_table f
left join
    sw_test.exchange_rates er
    on lower(f.currency) = er.currency_code
    and toDate(f.event_time) = er.rate_date  -- ensure date match using toDate() function for conversion
where
    f.event_name = 'payment';  -- filter for payment events only
