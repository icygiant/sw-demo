## Prerequisites:

* ```uv```

* ```python 3.12```

* ```psql```


## Project Setup:

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency and environment management.

To replicate the environment, clone the project, cd to this folder and run the following:

```bash
uv venv
uv sync
```
Create an `.env` file with all the necessary environment variables and use `connect.sh` to connect to your pg instance. Execute queries/DDL scripts in `data/`, then in `preaggregations/` and finally in `analytical_queries/`.
