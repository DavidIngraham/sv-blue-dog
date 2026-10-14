# SysML/Python project template

This package-less uv project is an independent starting point for a SysML-backed Python application. `Thermal::JouleHeat` is exported through `pyproject.toml` as `joule_heat`; there is no handwritten calculation adapter. It has no boat geometry, requirements or evidence-store dependency.

The current backend requires Linux, GCC and an explicitly selected OpenSysML executable. In this repository, set `OPENSYSML_BINARY` to the absolute path of the pinned compiler and run from this directory:

```sh
uv sync
uv run pytest -q
```

The tests prepare the declared exports and check the model's resistance default, a caller override, shared/per-case batch execution, invalid-input rejection and the model-defined positive-resistance check. For application use:

```python
from sysml_python import Project, execution_session
Project("pyproject.toml").prepare()
from generated import joule_heat

with execution_session() as run:
    print(joule_heat(current=2).power)
    print(joule_heat.batch(shared={"resistance": 5}, cases={"current": [1, 2, 3]}).values)
print(run.to_mapping())
```

## Start another project

Copy `.gitignore`, `models`, `tests` and `pyproject.toml` to a new project directory. Rename the project in `pyproject.toml`. Remove the `[tool.uv.sources]` section that points to this repository's editable package, then select your built wheel with `uv add /absolute/path/to/sysml_python_runtime-0.1.0-py3-none-any.whl`. The runtime has not been published to a package index. Use `uv sync` and `uv run pytest` to manage and test the new environment.

Replace the thermal model with your calculations and update `[tool.sysml_python.exports]`. The model supplies the numerical schema; an export supplies its qualified name and any explicit default/check bindings. Keep application scenarios and engineering decisions in the application. Do not commit generated Python/C files, compiler caches, `.venv` or `__pycache__`.

## Independence check

The repository CI builds a wheel, copies this template into a temporary directory outside the checkout, creates a fresh environment, installs that wheel and pytest, and runs these tests. This exercises the installed package rather than an editable source checkout. Preparation still requires the selected compiler; the wheel does not bundle OpenSysML or GCC.
