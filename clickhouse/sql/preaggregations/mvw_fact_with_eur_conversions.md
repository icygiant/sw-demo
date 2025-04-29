# 💶 Materialized View: EUR Conversion for Payments

I am creating a materialized view to **preconvert "payment" event amounts into EUR** using my exchange rate table — should be great for performance, especially when reporting or analytics depend on a standardized currency.

---

## 📑 Column Breakdown (Output)

| Column          | Type Inferred       | Description                                                          |
|------------------|---------------------|----------------------------------------------------------------------|
| `event_id`        | `UInt64`            | From `fact_table`, identifying the event
| `user_id`        | `UInt64`            | From `fact_table`, identifying the player                            |
| `amount`         | `Decimal(10,2)`     | Raw event amount (unconverted)                                      |
| `event_time`     | `DateTime`          | Timestamp of the event                                              |
| `currency`       | `Nullable(String)`  | Original currency string                                            |
| `amount_in_eur`  | `Float64`           | Converted value using `rate_to_eur`; falls back to raw amount       |
| `event_name`     | `LowCardinality(String)` | Type of event (only `'payment'` allowed by WHERE clause)          |

---

## ⚙️ Engine: `MergeTree()`

- Works well for append-only views like this.
- No deduplication logic seems to be needed since we're only reading from `fact_table`, which already uses `ReplacingMergeTree`.

🧠 Suggestion: If `fact_table` can be expected to get late updates, which I naturally want reflected here, I would go for **`ReplacingMergeTree(ingest_time)`** as the view engine as well.

---

## 🗂 Partitioning: `PARTITION BY toYYYYMM(event_time)`

- I think this is a solid choice for time-based reporting or filtering.


---

## 🔃 Ordering: `ORDER BY (event_id)`

- Great for time series analysis per user and segmentation.
- Helps with compression and query speed -  we can expect to group/filter by user and event_name as well as on time-granular columns. Also can expect to join back to the main fact_table and this should speed up such joins.

---