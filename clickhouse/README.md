# 🛠️ Local ClickHouse Setup (Docker)

This project provides a lightweight, laptop-safe ClickHouse environment, set up via Docker Compose.

The `docker-compose.yaml` file is located in the `docker/` folder.

---

## ✅ Prerequisites

Make sure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- `clickhouse-client`

---

## ⚙️ ClickHouse Configuration

- **Logging**:
  - Logging level set to `information` — only necessary details are logged.
  - Log file size capped at **100MB** to prevent excessive disk usage.
  - **3 logs** retained for rotation.

- **Listen Host**:
  - Bound to `127.0.0.1` (localhost) to ensure ClickHouse is not exposed externally.

- **ClickHouse Keeper**:
  - Internal lightweight ZooKeeper replacement (`Keeper`) enabled.
  - Listens on `localhost:9181`.
  - Used for local **ReplicatedMergeTree** testing (optional for replication experiments).

- **Distributed DDL Path**:
  - Configured even in single-node mode, enabling distributed DDL testing if needed.

- **Performance Optimizations**:
  - Lightweight testing/dev environment.
  - Minimal memory/disk impact.
  - Safe for use on machines with **4GB RAM**.
  - Quick spin-up and teardown.
  - Smaller log file size limits to avoid SSD bloat.

---

## 👤 Users Configuration

- **Access**:
  - Default user **without password**.
  - All IPs allowed (`::/0`), assuming local-only use.

- **Query Resource Limits**:
  - `max_memory_usage`: **2GB** per query.
  - `max_threads`: **2 threads** max (protects your CPU).
  - `load_balancing`: `in_order` (suitable for simple distributed setups).
  - `max_partitions_per_insert_block`: **50** (prevents overhead on small partition inserts).
  - `max_bytes_before_external_group_by`: **10MB** (spill to disk allowed for big `GROUP BY` operations).
  - `use_uncompressed_cache`: **disabled** (saves memory).

- **Quotas**:
  - **No enforced limits** (0 = unlimited), ideal for dev/testing.

- **Query Logging**:
  - Enabled by default.
  - Can be disabled if disk I/O becomes a bottleneck.

---

## 🗄️ Keeper Configuration

- Only listens on `localhost`.
- Extremely small log files.
- Fast timeouts.
- Minimal memory footprint.

> **Note:**  
> If you are **not using Replicated tables**, you can **disable Keeper** entirely!

---

## 🚀 Getting started

Spin up the instance by navigating to the docker/ folder and running:

```bash
docker compose up
```

Connect using the native ClickHouse client:

```bash
clickhouse-client --host 127.0.0.1 --port 9000
```