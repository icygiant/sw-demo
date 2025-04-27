CREATE TABLE sw_test.exchange_rates (
    currency_code TEXT NOT NULL,
    rate_to_eur NUMERIC(18,6) NOT NULL, -- Precision matters for currencies!
    rate_date DATE NOT NULL,
    PRIMARY KEY (currency_code, rate_date)
);
