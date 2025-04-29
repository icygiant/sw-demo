with first_install as (
    select * from sw_test.mvw_first_installs
)

, login_data as (
    select
        dh.user_id
        , uniqMerge(event_count) as count_logins  -- counting unique login events
    from sw_test.mvw_user_daily_history dh
    inner join first_install i on dh.user_id = i.user_id
    where dh.event_name = 'login'
      and dh.event_date >= i.install_date
      and dh.event_date < i.install_date + interval 4 week
    group by 1
)

, payment_data as (
    select
        dh.user_id
        , uniqMerge(event_count) as count_payments  -- counting unique payment events
    from sw_test.mvw_user_daily_history dh
    inner join first_install i on dh.user_id = i.user_id
    where dh.event_name = 'payment'
      and dh.event_date >= i.install_date
      and dh.event_date < i.install_date + interval 4 week
    group by 1
)

select
    round(avg(ld.count_logins)) as avg_logins
    , round(avg(pd.count_payments)) as avg_payments
from login_data ld
left join payment_data pd on ld.user_id = pd.user_id;

-- full outer join payment_data using (user_id);

--we could go for this not to miss users who only login or only pay.
--however, such cases wouldn't make any business sense 
--and would warrant investigations regarding bugs on the backend side 
-- I would enforce quality checks way earlier in the pipeline to flag such users