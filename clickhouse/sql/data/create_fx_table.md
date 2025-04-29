## 📑 Column Breakdown

| Column           | Type                         | Description                                                                 |
|------------------|------------------------------|-----------------------------------------------------------------------------|
| `currency_code`  | `LowCardinality(String)`     | Currency ISO code (e.g., `"USD"`, `"EUR"`). LowCardinality is great here.   |
| `rate_to_eur`    | `Float64`                    | Exchange rate to EUR. Using `Float64` gives higher precision.              |
| `rate_date`      | `Date`                       | Date when this rate was applicable. Daily granularity assumed.             |

---

## ⚙️ Engine: `ReplacingMergeTree()`

- This is a **great choice** for slowly changing dimensions (like exchange rates).
- Ensures only the **latest version** of a `(currency_code, rate_date)` pair remains.
- No versioning column is specified, so the **last inserted row wins**, which is okay for static or manually updated data.

---

## 🗂 Partitioning: `PARTITION BY toYYYYMM(rate_date)`

- Efficient for **time-bounded queries**.
- Monthly partitions work well with low update frequency.
- Keeps partitions compact while enabling pruning by date filters.

---

## 🔃 Ordering: `ORDER BY (currency_code, rate_date)`

- Facilitates:
  - Fast lookups like `WHERE currency_code = 'JPY' AND rate_date = '2005-05-01'`
  - Deduplication merges
- Matches natural access patterns in **analytical joins**.

---

## ✅ Use-Case Fit

I am really simplifying the implementation here by:
- Using a **single rate per currency** (e.g., only `JPY → EUR`)
- Restricting to a specific date range
- Avoiding true FX histories or multi-currency chaining

---

## 💡 Suggestions for Production-Grade Scenarios

- **Add a surrogate primary key** or a `UUID` column if the table gets versioned externally
- Track `source`/`vendor` (e.g., ECB, ForexAPI)
- Handle multiple rates per day (e.g., hourly FX changes)
- Include metadata fields like `is_valid`, `created_at`, or `ingestion_id` for auditability

---
