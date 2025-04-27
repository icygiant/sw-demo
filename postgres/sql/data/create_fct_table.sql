CREATE SCHEMA IF NOT EXISTS sw_test;
SET search_path TO sw_test;

CREATE TABLE IF NOT EXISTS sw_test.fact_table (
    user_id BIGINT,  -- Using BIGINT for 64-bit unsigned integer equivalent
    event_name TEXT,  -- String type, no LowCardinality equivalent, so we'll use TEXT
    event_time TIMESTAMP,  -- Using TIMESTAMP (Postgres' equivalent of DateTime)
    currency TEXT,  -- TEXT for nullable string values (nullable)
    amount NUMERIC(10, 2)  -- NUMERIC type with precision for financial data
);

CREATE INDEX idxuser_event_time ON sw_test.fact_table (user_id, event_time);
