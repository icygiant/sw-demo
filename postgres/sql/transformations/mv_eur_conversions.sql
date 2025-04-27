-- step 1: create a materialized view to pre-aggregate exchange rates and transaction data
create materialized view sw_test.mvw_fact_with_conversions as
select
    f.user_id,
    f.amount,
    f.event_time,
    f.currency,
    -- join with the exchange rates table to convert non-eur currencies
    coalesce(f.amount * er.rate_to_eur, f.amount) as amount_in_eur,
    f.event_name
from
    sw_test.fact_table f
left join
    sw_test.exchange_rates er
    on lower(f.currency) = er.currency_code
    and f.event_time::date = er.rate_date
where
    f.event_name = 'payment'; -- filter for payment events only
