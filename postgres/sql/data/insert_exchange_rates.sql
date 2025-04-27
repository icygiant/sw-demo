-- step 1: insert the fixed exchange rate for jpy to eur into the exchange_rates table
-- the rate of 0.0061 will be used for all dates in the specified range

do $$
declare
    start_date date := '2005-05-01';
    end_date date := '2005-12-14';
    current_date_var date;
begin
    current_date_var := start_date;
    
    -- loop through each date in the range
    while current_date_var <= end_date loop
        insert into sw_test.exchange_rates (currency_code, rate_to_eur, rate_date)
        values ('jpy', 0.0061, current_date_var)
        on conflict (currency_code, rate_date) 
        do update 
            set rate_to_eur = excluded.rate_to_eur; -- avoid duplicates
        
        current_date_var := current_date_var + interval '1 day'; -- increment the date by 1 day
    end loop;
end $$;
