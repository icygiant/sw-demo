-- calculating payment sums for the next 7 and 30 days, aggregated by day of life

with install_data as (
    select
        user_id,
        event_time as install_time,
        row_number() over (partition by user_id order by event_time) as rn
    from sw_test.fact_table
    where event_name = 'install'
)

, first_install as (
    select
        user_id,
        install_time
    from install_data
    where rn = 1  -- only take the first install event for each user
)

, payment_data as (
    select
        f.user_id,
        f.event_time as payment_time,
        -- calculate the 'day of life' for the payment
        toDateDiff(f.event_time, i.install_time, 'day') + 1 as day_of_life
    from sw_test.fact_table f
    join first_install i on f.user_id = i.user_id
    where f.event_name = 'payment'
)

, payment_sums as (
    select
        pd.user_id,
        pd.day_of_life,
        -- sum of payments in the next 7 days
        sum(p2.amount_in_eur) as sum_7_days,
        -- sum of payments in the next 30 days
        sum(p3.amount_in_eur) as sum_30_days
    from payment_data pd
    join sw_test.mvw_fact_with_conversions p2
        on pd.user_id = p2.user_id
        and p2.event_time > pd.payment_time
        and p2.event_time <= pd.payment_time + interval 7 day
    join sw_test.mvw_fact_with_conversions p3
        on pd.user_id = p3.user_id
        and p3.event_time > pd.payment_time
        and p3.event_time <= pd.payment_time + interval 30 day
    group by
        pd.user_id,
        pd.day_of_life
)

select
    ps.day_of_life,
    round(avg(ps.sum_7_days)) as avg_sum_7_days,
    round(avg(ps.sum_30_days)) as avg_sum_30_days
from payment_sums ps
where ps.day_of_life <= 10
group by ps.day_of_life
order by ps.day_of_life;
