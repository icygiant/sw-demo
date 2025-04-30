# Task 1 - SQL:

* The queries themselves are in `clickhouse/sql/analytical_queries.`

* The query results are in `clickhouse/QueryResults.md`

* Query 2 and 3 have two alternative options, the one with the suffix _optimized relies on cascading materialized views. Naturally, with the toy setup (small dataset and lean clickhouse environment) we have here, there were no substantial performance differences in terms of speed. So, one would be expected to benchmark these in prod-like conditions before deploying anything.

* `postgres/` contains a simple project that relies on a free pg instance hosted with Aiven to sanity check the clickhouse setup. Instructions on how to replicate the postgres project environment to test stuff locally without instantiating a clickhouse build are in `postgres/README.md`

# Task 2 - A/B Testing.

## 1. Frequentist A/B testing analysis:

* The Jupyter notebook containing the visualisations, the analysis and the interpretation of results is `ab_testing/freq/notebooks/main.ipynb`

## 2. Bayesian A/B testing analysis:

* The Jupyter notebook containing the visualisations, the analysis and the interpretation of results is `ab_testing/bayesian/notebooks/main.ipynb`
