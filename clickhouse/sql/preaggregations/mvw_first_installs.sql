create table sw_test.first_installs(
    user_id UInt64,
    install_date Date
)
engine = MergeTree() order by (user_id); --no need for ReplacingMergeTree() as the fact table is already deduped

create materialized view sw_test.mvw_first_installs to sw_test.first_installs
as
select
    user_id
    , min(ToDate(event_time)) as install_date
from sw_test.fact_table
where event_name = 'install'
group by 1;