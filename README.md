# PyInit

Initialize Python projects

This script generates the following project structure:

```
.
├── main.py
├── pyproject.toml
├── .gitignore
├── README.md
├── venv (if --venv arg is used)
├── setup.cfg
└── package/
    └── src/
        └── __init__.py
```


# How to use

1. Clone the repository
2. Install it with `pip install -e .`
3. Call the script with `pyinit`

# Arguments:

- `--venv`
    - creates a virtual environment for the project
- `-y`
    - creates the project with default values