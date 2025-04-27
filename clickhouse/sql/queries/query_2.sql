-- calculating average logins and payments in the first 4 weeks after the install event

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
    where rn = 1  -- selecting the first install event for each user
)

, login_data as (
    select
        f.user_id,
        count(distinct f.event_time) as login_count  -- counting distinct login events
    from sw_test.fact_table f
    join first_install i on f.user_id = i.user_id
    where f.event_name = 'login'
      and f.event_time >= i.install_time
      and f.event_time < i.install_time + interval 4 week
    group by f.user_id
)

, payment_data as (
    select
        f.user_id,
        count(distinct f.event_time) as payment_count  -- counting distinct payment events
    from sw_test.fact_table f
    join first_install i on f.user_id = i.user_id
    where f.event_name = 'payment'
      and f.event_time >= i.install_time
      and f.event_time < i.install_time + interval 4 week
    group by f.user_id
)

select
    round(avg(ld.login_count)) as avg_logins,
    round(avg(pd.payment_count)) as avg_payments
from login_data ld
join payment_data pd on ld.user_id = pd.user_id;
