-- explain analyze
with base as (
    select
        user_id
        , amount_in_eur
        , event_time
        , row_number() over (partition by user_id, event_time order by event_time desc) as rn
    from sw_test.mvw_fact_with_conversions
    where event_name = 'payment'   
)

, deduped as (
    select *
    from base
    where rn = 1
)

, ranked_base as (
    select
        *
        , row_number() over (partition by user_id order by event_time) as payment_sequence
    from deduped
)

, final as (
    select
        round(sum(amount_in_eur)) as sum_amount_paid_eur
    from ranked_base
    where payment_sequence between 2 and 7
)

select * from final
