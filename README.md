# SE-for-Sci -- Homework 1

This problem has 3 parts.

## Part I

In this repository, we have the following directories:
In this part, we will set up the packaging for this repository.

- `example` - The source code for an example project. You will modify `example/rk4.py` in [part II](#part-ii).
- `tests` - A directory containing tests, which may be helpful to you when modifying code. You do not need to modify this directory. Testing will be covered next week.

### Task 1

Create a `pyproject.toml` file containing

- A build backend. `hatchling` is recommended, but any one should work.
- A project table with `name`, `version`, `requires-python`, and `dependencies`.
  - The name needs to be `"example"`; some backends (like hatchling) will look for a package with the same name.
  - There should only be one dependency: [`numpy`](https://numpy.org/).
- An `dependency-groups` table with a `dev` extra (dependencies [`pytest`](https://docs.pytest.org/en/stable/), and [`plotext`](https://pypi.org/project/plotext/)).

This project now can be run with `uv run` if you have [`uv`](https://docs.astral.sh/uv/).

> If you want to set up a `.venv` folder yourself, use `uv sync` (`uv run` does this for you).
> ?
> If you really want to do it manually without `uv`:
>
> ```bash
> python -m venv .venv
> source .venv/bin/activate
> pip install -e. --group dev
> ```
>
> (You might need to update pip to use `--group`, `pip install -U pip`)

The development group contains pytest, so you can do `uv run pytest`.

### Task 2

Ruff's linter helps organize and debug code. We can write a ruleset into `pyproject.toml` so that every developer operates with the same set of rules.

Configure `ruff` by adding the following to your `pyproject.toml`.

```[toml]
[tool.ruff.lint]
extend-select = [
  "B",           # flake8-bugbear
  "I",           # isort
  "ARG",         # flake8-unused-arguments
  "C4",          # flake8-comprehensions
  "EM",          # flake8-errmsg
  "ICN",         # flake8-import-conventions
  "ISC",         # flake8-implicit-str-concat
  "G",           # flake8-logging-format
  "PGH",         # pygrep-hooks
  "PIE",         # flake8-pie
  "PL",          # pylint
  "PT",          # flake8-pytest-style
  "PTH",         # flake8-use-pathlib
  "RET",         # flake8-return
  "RUF",         # Ruff-specific
  "SIM",         # flake8-simplify
  "T20",         # flake8-print
  "UP",          # pyupgrade
  "YTT",         # flake8-2020
  "EXE",         # flake8-executable
  "NPY",         # NumPy specific rules
  "PD",          # pandas-vet
  "ERA",         # eradicate
]
ignore = [
  "PLR",    # Design related pylint codes
  "ISC001", # Conflicts with formatter
]
flake8-unused-arguments.ignore-variadic-names = true

[tool.ruff.lint.per-file-ignores]
"example/shm_error_analysis.py" = ["T201"]
```

We can run the linter with `uvx ruff check` (you can install ruff if you perfer, such as with `uv tool install ruff`).
Some rules have automatic fixes (for example, `isort` will automatically sort imports) that can be employed with `ruff check --fix`.
Additionally, some applications (like VS-Code) can be configured to highlight text where rules are broken. This is where those squiggly lines come from.

### Task 3

Add a `tool.pytest.ini_options` table for `pytest` to `pyproject.toml`.

`pytest tests` should run without errors.

Instead of adding the arguments to the `pytest` command, you can specify them here. An example is given [here](https://henryiii.github.io/se-for-sci/content/week03/pytest.html#running-and-configuring-pytest), which is also listed below for convenience:

```[toml]
[tool.pytest.ini_options]
minversion = "7.0"
addopts = ["-ra", "--strict-markers", "--strict-config"]
xfail_strict = true
filterwarnings = ["error"]
log_cli_level = "INFO"
testpaths = ["tests"]
```

## Part II

Fix the formatting of `example/rk4.py`. Before you submit, `ruff check` should not raise any issues. Additionally,

- Drop unneeded characters, like the `.` or `.0` after values (unless you explicitly want an float, such as in a definition), or the `0,` in a `range(0, x)`, or parenthesis around return statements.
- Add docsstrings to functions.
- In `solve()`, `_step()` is called twice per loop. Reduce it to one by either using temporary variables or utilizing `numpy` vectorization syntax.

The code should still produce the same results. `ruff format` may also be of help. You may notice that `ruff format` behaves differently from `ruff check --fix`. They are different tools and not aliases of each other. If you are using VS-Code it is possible to configure `ruff format` as the formatter for python files, which can be run using a hotkey.

As you work, `pytest` may be helpful to verify that no code-breaking changes are made. `example/shm_error_analysis.py` is already formatted.

## Hints

For the first parts, some good resources are:

- Week 5 of the course material
- [Scientific Python Library Development Guide](https://learn.scientific-python.org/development/guides/)
- [Packaging user guide](https://packaging.python.org/en/latest/)
- [INTERSECT Packaging workshop](https://intersect-training.org/packaging/)
