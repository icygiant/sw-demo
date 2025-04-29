with first_install as (
    select
        user_id
        , min(event_time) as install_time
    from sw_test.fact_table
    where event_name = 'install'
    group by user_id
)

, payment_data as (
    select
        f.user_id
        , f.event_time
        , coalesce(mv.amount_in_eur, 0) as amount_in_eur
        , ToDateDiff(f.event_time, i.install_time, 'day') + 1 as day_of_life
    from sw_test.fact_table
    inner join first_install i on f.user_id = i.user_id
    left join sw_test.mvw_fact_with_eur_conversions mv
        on mv.event_id = f.event_id
      and f.event_time < i.install_time + interval 30 day
)

, payment_sums as (
    select
        user_id
        , day_of_life
        , sumIf(amount_in_eur, day_of_life between 1 and 7) as sum_7_days
        , sumIf(amount_in_eur, day_of_life between 1 and 30) as sum_30_days
    from payment_data
    group by user_id, day_of_life
)

select
    day_of_life
    , round(avg(sum_7_days)) as avg_sum_7_days
    , round(avg(sum_30_days)) as avg_sum_30_days
from payment_sums
where day_of_life <= 10
group by day_of_life
order by day_of_life;
