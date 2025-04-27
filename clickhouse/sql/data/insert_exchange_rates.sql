-- step 1: insert the fixed exchange rate for jpy to eur into the exchange_rates table
-- the rate of 0.0061 will be used for all dates in the specified range

insert into sw_test.exchange_rates (currency_code, rate_to_eur, rate_date)
select 
    'jpy' as currency_code,
    0.0061 as rate_to_eur,
    dateAdd('day', number, '2005-05-01') as rate_date  -- generates dates starting from '2005-05-01'
from numbers(toUInt32(dateDiff('day', '2005-05-01', '2005-12-14')))  -- generate a sequence of numbers to calculate days between the start and end date
