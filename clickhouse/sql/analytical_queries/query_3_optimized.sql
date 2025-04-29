with first_install as (
    select * from sw_test.mvw_first_installs
)

, payment_data as (
    select
        mv.user_id
        , ToDateDiff(mv.event_date, i.install_date, 'day') + 1 as day_of_life
        , mv.total_amount_eur
        , mv.event_count
    from sw_test.mvw_user_daily_history mv
    inner join first_install i on mv.user_id = i.user_id
)

, payment_data_30_days as (
    select * from payment_data
    where day_of_life <= 30
)

, payment_sums as (
    select
        user_id
        , day_of_life
        , sumMergeIf(total_amount_in_eur, day_of_life between 1 and 7) as sum_7_days
        , sumMergeIf(total_amount_in_eur, day_of_life between 1 and 30) as sum_30_days
    from payment_data
    group by 1, 2
)

select
    day_of_life
    , round(avg(sum_7_days)) as avg_sum_7_days_eur
    , round(avg(sum_30_days)) as avg_sum_30_days_eur
from payment_sums
where day_of_life <= 10
group by 1
order by 1;
