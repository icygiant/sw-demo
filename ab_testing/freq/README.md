## Prerequisites:

* ```uv```

* ```python >= 3.12```

The project also expects the local path to the data file (```file_path```) to be set as an environment variable. I recommend sourcing it via an ```.env``` file.

## Project Setup:

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency and environment management.

To replicate the environment, clone the project, cd to this folder and run the following:

```bash
uv venv
uv sync
```