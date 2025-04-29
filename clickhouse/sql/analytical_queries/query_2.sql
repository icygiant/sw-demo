with first_install as (
    select
        user_id
        , min(event_time) as install_time
    from sw_test.fact_table
    where event_name = 'install'
    group by user_id
)

, login_data as (
    select
        f.user_id
        , count(distinct f.event_id) as login_count  -- counting unique login events
    from sw_test.fact_table f
    inner join first_install i on f.user_id = i.user_id
    where f.event_name = 'login'
      and f.event_time >= i.install_time
      and f.event_time < i.install_time + interval 4 week
    group by f.user_id
)

, payment_data as (
    select
        f.user_id
        , count(distinct f.event_id) as payment_count  -- counting distinct payment events
    from sw_test.fact_table f
    inner join first_install i on f.user_id = i.user_id
    where f.event_name = 'payment'
      and f.event_time >= i.install_time
      and f.event_time < i.install_time + interval 4 week
    group by f.user_id
)

select
    round(avg(ld.login_count)) as avg_logins
    , round(avg(pd.payment_count)) as avg_payments
from login_data ld
left join payment_data pd on ld.user_id = pd.user_id;
-- full outer join payment_data using (user_id);

--we could go for this not to miss users who only login or only pay.
--however, such cases wouldn't make any business sense 
--and would warrant investigations regarding bugs on the backend side 
-- I would enforce quality checks way earlier in the pipeline to flag such users