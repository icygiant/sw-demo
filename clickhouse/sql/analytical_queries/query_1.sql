with base as (
    select
        user_id
        , amount_in_eur
        , event_time
    from sw_test.mvw_fact_with_eur_conversions   
)

, ranked_base as (
    select
        *
        , row_number() over (partition by user_id order by event_time) as payment_sequence
    from base
)

, final as (
    select
        round(sum(amount_in_eur)) as sum_amount_paid_eur
    from ranked_base
    where payment_sequence between 2 and 7
)

select * from final
