# 📦 ClickHouse Table Design: `fact_table`

This table is optimized for **microbatch ingestion** of online game events (e.g., from a Total Battle-like backend), with support for **late-arriving events**, **deduplication**, and efficient querying.

---


# 📑 Column Breakdown

| Column        | Type                                  | Description                                                                 |
|---------------|----------------------------------------|-----------------------------------------------------------------------------|
| `user_id`     | `UInt64`                               | Unique player/user ID                                                      |
| `event_name`  | `LowCardinality(String)`               | Event type (e.g., `"install"`, `"login"`)                          |
| `event_time`  | `DateTime`                             | In-game timestamp of the event                                             |
| `currency`    | `LowCardinality(Nullable(String))`     | Optional currency or virtual economy tag                                   |
| `amount`      | `Decimal(10, 2)`                        | Money or virtual currency amount with 2 decimal precision                  |
| `ingest_time` | `DateTime DEFAULT now()`               | Server-side ingestion timestamp (used for deduplication versioning)        |
| `event_id`    | `UInt64 MATERIALIZED ...`              | Deterministic hash for deduplication (`sipHash64(user_id + time + name)`) |

---

`event_id` is repeatable, `UInt` hash ensures better sorting and compression performance than `UUID`. It also has a smaller data footprint than `UUID` (8 bytes versus 16). We don't have to insert it, Clickhouse will compute it on the fly (hence, `MATERIALIZED`). Since I am working with semi-structured game events that can replay, hash collisions here are really unlikely and global uniqueness is not needed (row-level is fine), I think it makes sense to define it as a hash of `user_id`, `event_time` and `event_name` - this makes deduplication consistent and deterministic.

# ⚙️ Engine: `ReplacingMergeTree(ingest_time)`

- Used for **deduplication** based on a key (here, `event_id`)
- Keeps the **latest row** per `event_id` based on `ingest_time`
- Ideal for pipelines where:
  - Events may arrive more than once
  - Retries or delays are possible
  - You want **idempotent ingestion**

---

# 🗂 Partitioning: `PARTITION BY (event_name)`

- Creates separate partitions per event type
- We can expect to often filter/group by event too so this is useful.
- 🧠 Ok to only if `event_name` has **low cardinality** - this is true at least in the data I already bulk-inserted.
  - One could always switch to smth like `toYYYYMM(event_time)` later on if event variety grows too large.

---

# 🔃 Ordering: `ORDER BY (event_id)`

- Orders rows by deterministic ID, ensuring:
  - ⚡ Fast merges
  - ✅ Accurate deduplication
- ClickHouse can **efficiently skip** over blocks when querying
- We can expect to often filter/group by event too so this is useful.
---

# 🧪 Sampling: `SAMPLE BY ()`

- Skipped as "sample queries" are unlikely

---

# 📏 Index Granularity: `index_granularity = 8192`

- Controls how frequently primary index marks are written
- Tradeoff between:
  - 🔍 Query precision
  - 📦 Storage size
- 8192 is a safe, balanced default for wide-row fact tables

---

# 🧠 Design Benefits

- 🔄 **Idempotent writes**: duplicate events won’t accumulate
- 🚀 **Fast inserts**: MergeTree-based engines are optimized for high-throughput batch ingestion
- 🧹 **Clean deduplication**: using `event_id` ensures semantic uniqueness
- 🔎 **Smart filtering**: partitioning and indexing make queries fast even as data grows

---

✅ Ideal for streaming or microbatch pipelines like:

**Backend service → Kafka producer → Kafka Broker ⇔ Kafka consumer → (Spark) → ClickHouse**

With support for upserts, game telemetry, and financial event tracking.
